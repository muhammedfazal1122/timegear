from django.urls import path
from . import views

app_name = 'category'


urlpatterns = [

    path('admn_product_category/', views.admn_product_category, name='admn_product_category'),
    path('admn_add_category/', views.admn_add_category, name='admn_add_category'),
    path('admn_edit_category/<int:id>/', views.admn_edit_category, name='admn_edit_category'),
    path('admn_delete_categories/<int:id>/', views.admn_delete_categories, name='admn_delete_categories'),
    path('admn_enable_disable_categories/<int:id>/', views.admn_enable_disable_categories, name='admn_enable_disable_categories'),



    path('shop_by_category/<str:category_name>/', views.shop_by_category, name='shop_by_category'),

]


