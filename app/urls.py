from django.urls import path
from app import views

app_name='app'

urlpatterns = [
    path('',views.index,name="index"),


    path('admn_users_list/', views.admn_users_list, name='admn_users_list'),
    path('admn_users_block_unblock/<int:id>', views.admn_users_block_unblock, name='admn_users_block_unblock'),

]
