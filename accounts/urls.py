from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('user-login',views.user_login,name="user-login"),
    path('user-logout',views.user_logout,name="user-logout"),
    path('register',views.register,name="register"),
    path('forgotpassword',views.forgotpassword,name="forgotpassword"),
    # path('otp-regis/', views.otp_regis, name='otp-regis'),



    path('sent-otp',views.sent_otp,name='sent-otp'),
    path('verify-otp',views.verify_otp,name='verify-otp'),
    path('resend',views.resend_otp,name='resend-otp'),
   
    # path('forgot_password/', views.forgot_password, name='forgot_password'),
    # path('verify-otp/forgot_password',views.verify_otp_forgot_password,name='verify-otp-forgot-password'),
    # path('sent-otp/forgot_password',views.sent_otp_forgot_password,name='sent-otp-forgot-password'),
  

    ###############################  admin  ####################################

    
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name="admin_dashboard"),
    path('admin-logout/',views.admin_logout,name='admin_logout'),
     


]
