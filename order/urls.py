from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [

    path('order_placed/', views.order_placed, name='order_placed'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('online_payment/', views.online_payment, name='online_payment'),
    path('ordered_product_detailes/<int:order_id>/', views.ordered_product_detailes, name='ordered_product_detailes'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('update_status/', views.update_status, name='update_status'),
    path('admn_product_order/', views.admn_product_order, name='admn_product_order'),


#----------------------------------COUPEN------------------------------------------------#


    path('delete_coupon/<int:id>/', views.delete_coupon, name='delete_coupon'),
    path('admn_coupon_management/', views.AdmnCouponManagementView.as_view(), name='admn_coupon_management'),
    path('generate_code/', views.generate_code, name='generate_code'),
    path('apply_coupon/', views.apply_coupon, name='apply_coupon'),
    
    

]