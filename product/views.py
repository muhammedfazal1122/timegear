from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from .models import Product
from django.views.decorators.cache import cache_control
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from .models import Category
from django.utils.text import slugify
from django.contrib import messages
from brand.models import Brand


# Create your views here.


########################## user-PRODUCT ################################



@cache_control(no_cache=True,must_revalidate=True,no_store=True)   
def product_details(request, id):
    products=Product.objects.get(id=id)
    
    context={
        'products':products
    }
    return render(request, 'evara-frontend/shop-product-details.html',context)

########################## ADMIN-PRODUCT ################################

#-----------Product list-view page------------------
@login_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admn_product_list(request):
    products = Product.objects.all()
    
    context = {

        'products':products

    }
    return render(request, 'evara-backend/page-products-list.html',context)

@login_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admn_add_product(request):
    if request.method=="POST":
        print(request.POST)
        product_name=request.POST.get("product_name")
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)
        brand_id = request.POST.get("brand")
        brand=Brand.objects.get(id=brand_id)
        description=request.POST.get("description")
        price=request.POST.get("price")
        max_price=request.POST.get("max_price")
        if int(price) <0 or int(max_price) < 0:
            messages.warning(request, "Negative values are not allowed")
            return redirect('product:admn_add_product')
        stock=request.POST.get("stock")
        images=request.FILES.get('images')
        product_images2=request.FILES.get('product_images2')
        product_images3=request.FILES.get('product_images3')
        product_images4=request.FILES.get('product_images4')
        product_images5=request.FILES.get('product_images5')
        slug = slugify(product_name)
        count = 1

        while Product.objects.filter(slug=slug).exists():
            slug = f"{slug}-{count}"
            count += 1

        try:
            brand = Brand.objects.get(id=brand_id)
        except Brand.DoesNotExist:
            messages.warning(request, "Selected brand does not exist.")
            return redirect('product:admn_add_product')


        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            messages.warning(request, "Selected brand does not exist.")
            return redirect('product:admn_add_product')

           
        product=Product(
            product_name=product_name,
            category=category,
            brand=brand,
            description=description,
            price=price,
            max_price=max_price,
            stock=stock,
            slug=slug,
            images=images,
            product_images2=product_images2,
            product_images3=product_images3,
            product_images4=product_images4,
            product_images5=product_images5,
        )    
        print(product)
        product.save() 
        messages.success(request,'Product Added Succcessfully..')
        return redirect('product:admn_product_list')
    
    categories=Category.objects.all()
    brand=Brand.objects.all()
    context={
        'categories':categories,
        'brand':brand
    }
    return render(request, 'evara-backend/page-add-product.html',context)



@login_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admn_edit_product(request,id):
    product=Product.objects.get(id=id)
    categories=Category.objects.all()
    brand=Brand.objects.all()

    if request.method=='POST':

        product.product_name=request.POST.get('product_name')
        category_id=request.POST.get('category')
        product.category = Category.objects.get(id=category_id) 
        brand_id = request.POST.get('brand')
        product.brand=Brand.objects.get(id=brand_id) 
        product.description=request.POST.get('description')
        product.price=request.POST.get('price')
        product.max_price=request.POST.get("max_price")
        price_str = request.POST.get('price')

        try:
            price = float(price_str)
        except ValueError:
            messages.warning(request, "Price must be a valid number.")
            return redirect('product:admn_edit_product', id=id)

        if price < 0:
            messages.warning(request, "Price must be greater than or equal to 0")
            return redirect('product:admn_edit_product', id=id)
        
        product.stock=request.POST.get('stock')
        product.images=request.FILES.get('images')
        product.product_images2=request.FILES.get('product_images2')
        product.product_images3=request.FILES.get('product_images3')
        product.product_images4=request.FILES.get('product_images4')
        product.product_images5=request.FILES.get('product_images5')
        product.save()
        messages.success(request,'Product Edited Succcessfully..')
        return redirect('product:admn_product_list')
    return render(request, 'evara-backend/page-edit-products.html', {'product': product,'categories': categories, 'brand':brand})



#--------------Delete product--------------------------
@login_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admn_delete_product(request,id):
    product=get_object_or_404(Product,id=id)
    if product.soft_deleted:
        product.soft_deleted=False
        product.is_available=True

    else:
        product.is_available=False
        product.soft_deleted=True
    product.save()
    return redirect('product:admn_product_list')

def shop(request):

    products = Product.objects.all().filter(is_available=True)
    categories = Category.objects.all()
    context={
        'products':products,
        'categories':categories
    }

    return render(request,"evara-frontend/shop-list-left.html",context)

def shop_by_category(request, category_name):
    products = Product.objects.filter(category__category_name=category_name)
    return render(request, "evara-frontend/shop-list-left.html", {'products': products})





