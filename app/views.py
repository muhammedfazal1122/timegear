from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from product.models import Product
from django.views.decorators.cache import cache_control
from django.shortcuts import render,redirect
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from accounts.models import Account
from django.contrib import messages
from brand.models import Brand
from category.models import Category
from cart.models import Cart



# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    products = Product.objects.all().filter(is_available=True)
    brand = Brand.objects.filter(soft_deleted=False)
    categories = Category.objects.all()
    users = Account.objects.all()
    cart = Cart.objects.all()

    context = {
        'users':users,
        'products':products,
        'brand':brand,
        'categories':categories,
        'cart':cart,
    }
    
    return render(request,"evara-frontend/index.html",context)




#--------------------Admin side user list page------------
@login_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admn_users_list(request):
    users=Account.objects.all().exclude(is_superuser=True)
    context={
        'users':users
    }
    return render(request, 'evara-backend/page-users-list.html',context)

#------------------Admin side user block unblock-------------
@login_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admn_users_block_unblock(request,id):
    user=Account.objects.get(id=id)
    try:
        if user.is_blocked:
            user.is_blocked=False
            user.is_active=True
            user.save()
            messages.success(request, 'User  Unblocked')
        else:
            user.is_blocked=True
            user.is_active=False
            user.save()
            messages.warning(request, 'User is Blocked')
    except Account.DoesNotExist:
        messages.warning(request,'User does not Exist')
    return redirect('app:admn_users_list')    

