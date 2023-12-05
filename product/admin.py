from django.contrib import admin
from .models import Product
from .models import Variation


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','category','modified_date','is_available')
    prepopulated_fields = {'slug':("product_name",)}


admin.site.register(Product,ProductAdmin) 


class VariationAdmin(admin.ModelAdmin):
    list_display = ("product","variation_value","is_active","variation_category")
    list_editable = ("is_active",)
    list_filter = ("product","variation_value","variation_category",)

admin.site.register(Variation,VariationAdmin)

