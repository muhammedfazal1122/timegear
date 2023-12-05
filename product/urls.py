from django.urls import path
from . import views

app_name = 'product'


urlpatterns = [
    path('admn-product-list/',views.admn_product_list,name="admn_product_list"),
    path ('admn-add-product/',views.admn_add_product,name="admn_add_product"),
    path('admn_edit_product/<int:id>/', views.admn_edit_product, name='admn_edit_product'),
    path('admn_delete_product/<int:id>', views.admn_delete_product, name='admn_delete_product'),




    ########################### USER   #################################
    path('product-details/<int:id>/', views.product_details, name='product_details'),
    path('shop/', views.shop, name='shop'),
    path('shop_by_category/<str:category_name>/', views.shop_by_category, name='shop_by_category'),


]



