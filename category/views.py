from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from .models import Category
from product.models import Product
from accounts.models import Account
from django.contrib import messages
import re


# Create your views here.
@login_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admn_product_category(request):
    categories=Category.objects.all()
    context={
        'categories':categories
    }
    return render(request, 'evara-backend/page-categories.html',context)

@login_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admn_add_category(request):
    if request.method=="POST":
        category_name=request.POST.get("category_name")
        slug=request.POST.get("slug")
        description = request.POST.get("description", "")  # Default to an empty string if not provided
        discount=request.POST.get("discount")
        minimum_amount=request.POST.get("minimum_amount")
        end_date=request.POST.get("end_date")
        cat_image=request.FILES.get("cat_image")


        if any(char.isspace() or re.match('[@#$%^@%@#%&]', char) for char in category_name):
            messages.warning(request, "category name Must be Alphabet")
        elif any(char.isspace() or re.match('[@#$%^@%@#%&]', char) for char in slug):
            messages.warning(request, "slug Must be Alphabet")

        else:

            categories = Category(
                category_name=category_name,
                slug=slug,
                description=description,
                cat_image=cat_image,
                discount=discount,
                minimum_amount=minimum_amount,
                end_date=end_date,
            )
            categories.save()
            messages.success(request, 'Category Added Successfully')
            return redirect("category:admn_product_category")
    return render(request, "evara-backend/page-add-categories.html")  

        


def admn_edit_category(request,id):
    category=Category.objects.get(id=id)

    if request.method=='POST':
        category.category_name=request.POST.get('category_name')
        category.slug=request.POST.get('slug')
        category.description=request.POST.get('description')
        category.cat_image=request.FILES.get('cat_image')
        category.discount=request.POST.get('discount')
        category.minimum_amount=request.POST.get('minimum_amount')
        category.end_date=request.POST.get('end_date')

        category.save()
        return redirect('category:admn_product_category')
    context={
        'category':category
    }
    messages.success(request,"Category Edited successfully")
    return render(request, 'evara-backend/page-edit-categories.html',context)



@login_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admn_delete_categories(request,id):
    category= get_object_or_404(Category,id=id)
    category.delete()
    messages.success(request,"Category deleted successfully")
    return redirect('category:admn_product_category')



@login_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admn_enable_disable_categories(request,id):
    category=Category.objects.get(id=id)
    try:
        if category.soft_deleted:
            category.soft_deleted=False
            is_available=False
            category.save()
            messages.warning(request,'Category Disabled')
            return redirect('admn_product_category')
        else:
            category.soft_deleted=True
            is_available=True
            category.save()
            messages.success(request,'Category Enabled')
    except:
        pass
    return redirect('category:admn_product_category')

def shop_by_category(request, category_name):
    products = Product.objects.filter(category__category_name=category_name,is_available=True)
    return render(request, "evara-frontend/shop-list-left.html", {'products': products})


