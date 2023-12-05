from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from category.models import Category
from django.contrib import messages
from product.models import Product
from product.models import ProductVariation
from cart.models import Cart,CartItem
from django.http import HttpRequest, JsonResponse
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist
from user.models import AdressBook
from cart.models import Variation
from decimal import Decimal



# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart 


def add_cart(request,product_id):
    current_user = request.user

    if request.method=="POST":
        for item in request.POST:
            key = item
            value = request.POST[key]

    product = Product.objects.get(id=product_id)
    variation = Variation.objects.get(product=product,variation_value=value)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request), user=current_user) #get cart item  by using the cart_id present in session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request),
            user=current_user,
        )
    cart.save()
    try:
        cart_items = CartItem.objects.get(variations=variation, cart=cart, user=current_user)
        cart_items.quantity +=1
        cart_items.save()

    except CartItem.DoesNotExist:
        cart_items = CartItem.objects.create(
            product=product,
            cart=cart,
            variations=variation,
            quantity=1,
            user=current_user,  
            is_active=True,
        )

        cart_items.save()
    

    return redirect("cart:cart")


def cart(request,total=0,quantity=0,cart_items=None):
    try:
        category_discount_applyed=0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        # cart_items =  CartItem.objects.filter(cart=cart,is_active=True)
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)

        for cart_item in cart_items:
            category_discount = cart_item.product.category.discount

            if category_discount != 0:
                cart_item.product.price = getCatogoryPrice(cart_item)
                category_discount_applyed = cart_item.product.price

            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
           
    except :
        pass
    context = {
        
        "quantity":quantity,
        "total":total,
        "cart_items":cart_items,
        # "category_discount":category_discount,
        "category_discount_applyed":category_discount_applyed,

    }
   
   
    return render(request,"evara-frontend/shop-cart.html",context)





def Remove_cart_item(request,variations):
    
    cart = Cart.objects.get(user=request.user)
    variations = get_object_or_404(Variation, id=variations)
    cart_item = CartItem.objects.filter(variations=variations,cart=cart)
    cart_item.delete()
    return redirect('cart:cart')




def getCatogoryPrice(cart_item):
    category_discount = Decimal(cart_item.product.category.discount)
    category_minimum_amount = Decimal(cart_item.product.category.minimum_amount)
    price = Decimal(cart_item.product.price)
    end_date = cart_item.product.category.end_date

    # Check if the category end date is expired
    if not cart_item.product.category.is_expired() and category_minimum_amount < price:
        discounted_price = price - (price * (category_discount / 100))
        return discounted_price
    else:
        return price



def checkout(request, total=0, quantity=0, cart_items=None):
    current_user=request.user

    # category_product =  Category.objects.get
    if not current_user.is_authenticated:
        messages.warning(request, "User must log in for Checkout")
        return redirect('app:index')
    
    category_discound = request.POST.get("category_discound")
    

    try:
        grand_total = 0
        total = 0
        quantity = 0
        sub_total=0

        if current_user.is_authenticated:
            cart_items = CartItem.objects.filter(user=current_user, is_active=True)
        else:
            pass
        
        for cart_item in cart_items:
            category_discount = cart_item.product.category.discount

            if category_discount != 0:
                cart_item.product.price = getCatogoryPrice(cart_item)
                category_discount_applyed = cart_item.product.price
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            sub_total = (cart_item.quantity * cart_item.product.price)

        grand_total = total  # Apply coupon discount to grand_total

    except ObjectDoesNotExist as e:
        print("Error retrieving cart items:", e)

    address_list = AdressBook.objects.filter(user=current_user)
    # print("address_list:", address_list)

    default_address = address_list.filter(is_default=True).first()
    category = Category.objects.all()

    # print("default_address:", default_address)
    payment_method = request.POST.get('payment_option')
    print("Selected Payment Method:", payment_method)

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'grand_total': grand_total,
        'address_list': address_list,
        'default_address': default_address,
        'sub_total':sub_total,
        'category':category,

        
    }

    return render(request, 'evara-frontend/checkout2.html', context)


def add_address(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('account:index')
   
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address_line_1 = request.POST.get('address')
        # address_line_2 = request.POST.get('address_line_2')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        phone = request.POST.get('phone')



        #Create a new shipping address instance
        address = AdressBook(user=request.user,first_name=first_name,last_name=last_name,   phone=phone, address_line_1=address_line_1,  country=country, state=state, city=city, pincode=pincode)
        address.save()


        # Set is_default attribute of the newly added address and reset previous default
        if request.user.is_authenticated:
            AdressBook.objects.filter(user=request.user, is_default=True).update(is_default=False)
            address.is_default = True
            address.save()

        # if 'source' in request.GET and request.GET['source'] == 'checkout':
        #     # If the source is 'checkout', redirect back to the checkout page
        #     return redirect('user:checkout')  # Replace 'checkout' with your actual checkout view name

        return redirect('cart:checkout')




    


 
def newcart_update(request):
    new_quantity = 0
    total = 0
    tax = 0
    grand_total = 0
    quantity=0
    counter=0

    if request.method == 'POST' and request.user.is_authenticated:
        prod_id = int(request.POST.get('product_id'))
        cart_item_id = int(request.POST.get('cart_id'))
        qty=int(request.POST.get('qty'))
        counter=int(request.POST.get('counter'))
        product = get_object_or_404(Product, id=prod_id)
        try:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
            cart_items = CartItem.objects.filter(user=request.user)
        except CartItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Cart item not found'})
        
        if cart_item.product:
            variation = cart_item.variations  # Access the variation associated with the cart item

            if cart_item.quantity < product.stock:
                cart_item.quantity += 1
                cart_item.save()
                # total = cart_item.quantity * product.price
                # tax = (2 * total) / 100
                # grand_total = total + tax
                sub_total=cart_item.quantity * product.price
                new_quantity = cart_item.quantity
             
                
            else:
                return JsonResponse({'status': 'error', 'message': message})      
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax


    if new_quantity == 0:
        message = "out of stock"
        return JsonResponse({'status': 'error', 'message': message})
    else:
        return JsonResponse({

            'status': "success",
            'new_quantity': new_quantity,
            "total": total,
            "tax": tax,
            'counter':counter,
            "grand_total": grand_total,
            "sub_total":sub_total,
            
        })




def remove_cart_item_fully(request):
    new_quantity = 0
    total = 0
    tax = 0
    grand_total = 0
    quantity=0
    counter=0


    if request.method == 'POST' and request.user.is_authenticated:
       
        pro_id = int(request.POST.get('product_id'))
        cart_item_id = int(request.POST.get('cart_id'))
        qty=int(request.POST.get('qty'))
        counter = int(request.POST.get('counter'))       
        product = get_object_or_404(Product, id=pro_id)
        try:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
            cart_items = CartItem.objects.filter(user=request.user)
        except:
            return JsonResponse({"status":"error", 'message': 'Cart item not found' })
        if cart_item.product:
            variation = cart_item.variations

            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                new_quantity = cart_item.quantity

            else:
                # If the quantity is 1, delete the cart item
                pass
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax



    if new_quantity == 0:
        message = "Sorry, the quantity cannot be less than 1. If you want to remove this item, please use the 'Remove' option instead."
        return JsonResponse({'status': 'error', 'message': message})
    else:
        return JsonResponse({

            'status': "success",
            'new_quantity': new_quantity,
            "total": total,
            "tax": tax,
            'counter':counter,
            "grand_total": grand_total,
            
        })
    
def add_to_cart_icon(request, product_id, quantity=1):
    print('helo worlds')
    user = request.user
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart)

    if quantity > product.quantity:
        # Redirect to the previous page if quantity is greater than available stock
        redirect_url = request.META.get('HTTP_REFERER', '/')
        return redirect(redirect_url)

    if not created:
        cart_item.quantity += 1
        cart_item.save()
    else:
        cart_item.quantity = quantity
        cart_item.save()

    return JsonResponse({"success": True})
