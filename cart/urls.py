from django.urls import path
from . import views

app_name = 'cart'


urlpatterns = [
    
    path('cart/', views.cart, name='cart'), 
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),  
    path('add_to_cart_icon/<int:product_id>/', views.add_to_cart_icon, name='add_to_cart_icon'),  
 

    path('ajax/update/cart/', views.newcart_update, name='newcart_update'),
    path('ajax/remove/cart/', views.remove_cart_item_fully, name='remove_cart_item_fully'),
    path('checkout/', views.checkout, name='checkout'),
    path('add_address/', views.add_address, name='add_address'),
    path('Remove_cart_item/<int:variations>/', views.Remove_cart_item, name='Remove_cart_item'),


]


