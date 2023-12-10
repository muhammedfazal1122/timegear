from django.urls import path
from . import views
app_name = 'user'


urlpatterns = [
    path('manage_address/', views.manage_address, name='manage_address'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('add_address/', views.add_address, name='add_address'),
    path('delete_address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('edit_address/<int:address_id>/', views.edit_address, name='edit_address'),
    path('admn_sales_report/', views.admn_sales_report, name='admn_sales_report'),
    path('sales-report', views.sales_report, name='sales-report'),

#---------------------------- WALLET---------------------------------------#
    path('my_wallet', views.my_wallet, name='my_wallet'),

    # path('fetchData/month/', views.fetch_data_month, name='fetch_data_month'),
    # path('fetchData/week/', views.fetch_data_week, name='fetch_data_week'),
    # path('fetchData/year/', views.fetch_data_year, name='fetch_data_year'),


]
