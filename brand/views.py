from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.contrib.sessions.models import Session
from .models import Brand
from django.views import View
from django.http import Http404

# Create your views here.

class AdminBrandListView(View):
    template_name = "evara-backend/page-brands.html"

    def get(self, request):
        brand = Brand.objects.all()
        context = {
            'brand': brand
        }
        return render(request, self.template_name, context)
    

class AddBrandView(View):
    template_name = "evara-backend/add-Brand.html"  

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if request.method == 'POST':
            brand_name = request.POST.get("brand_name")
            brand_image = request.FILES.get('brand_image')
            brand = Brand.objects.create(brand_name=brand_name, logo=brand_image)
            brand.save()

        return redirect('brand:admn_brand_list') 



class EditView(View):
    template_name = "evara-backend/edit-Brand.html"

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        try:
            brand = Brand.objects.get(id=id)
        except Brand.DoesNotExist:
            raise Http404("Brand does not exist")

        context = {
            'brand': brand
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        id = kwargs.get('id')
        try:
            brand = Brand.objects.get(id=id)
        except Brand.DoesNotExist:
            raise Http404("Brand does not exist")

        if request.method == 'POST':
            brand.brand_name = request.POST.get("brand_name")
            brand.logo = request.FILES.get('brand_image')
            brand.save()
            messages.success(request, "Brand Edited successfully")

        return redirect('brand:admn_brand_list')


class AdmnEnableDisableBrandView(View):
    def get(self, request, id):
        brand = get_object_or_404(Brand, id=id)
        try:
            if brand.soft_deleted == False:
                brand.soft_deleted = True
                brand.save()
                messages.success(request, 'Category Disabled')
            else:
                brand.soft_deleted = False
                brand.save()
                messages.success(request, 'Category Enabled')
        except:
            pass

        return redirect("brand:admn_brand_list")