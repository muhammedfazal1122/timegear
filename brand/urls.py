from django.urls import path
from . import views

app_name = 'brand'

urlpatterns = [
    path('admn_brand_list', views.AdminBrandListView.as_view(), name='admn_brand_list'),
    path('add-admin-brand', views.AddBrandView.as_view(), name='add_brand'),
    path('edit-brand/<int:id>',views.EditView.as_view(),name="edit_brand"),
    path('admn_enable_disable_brand/<int:id>/', views.AdmnEnableDisableBrandView.as_view(), name='admn_enable_disable_brand'),

]