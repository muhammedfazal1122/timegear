from datetime import timedelta, timezone
from functools import wraps
from django.http import JsonResponse
import datetime
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import RegistrationForm
from .models import Account
from django.views.decorators.cache import cache_control
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import Account
from order.models import Order,OrderProduct
from user.models import Wallet,WalletTransaction
import pyotp
from product.models import Product
import re
# varification
# views.py
from django.core.mail import send_mail
import random
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model


# ------------------------------------------#forgot password#------------------------------

from django.utils.http import  urlsafe_base64_decode


# Create your views here.


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_protect
def user_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == "POST":
        email =request.POST['email']
        password = request.POST['password']

        if not Account.objects.filter(email=email).exists():
            messages.error(request, "Invalid Email Adress")
            return redirect('accounts:user-login')
        
        if not Account.objects.filter(email=email,is_active=True).exists():
            messages.error(request, "You are blocked by admin ! Please contact admin ")
            return redirect('accounts:user-login') 

        user=authenticate(request,email=email,password=password)

        if user:
            request.session.create()
            print('session key is:',request.session.session_key)
            request.session['email'] = email
            return redirect('accounts:sent-otp')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('accounts:user-login')
        
    return render (request,'evara-frontend/accounts/login.html')

User = get_user_model()  # Get the User model defined in your project


def sent_otp(request):
   random_num=random.randint(1000,9999)
   print("OOTTTPPP::",random_num)
   request.session['OTP_Key']=str(random_num)
   send_mail(
   "OTP AUTHENTICATING TimeMachine",
   f"{random_num} -OTP",
   "ecomm.apps.info@gmail.com",
   [request.session['email']],
   fail_silently=False,
    )
   return redirect('accounts:verify-otp')

from django.contrib import messages
from django.contrib.auth import login

def verify_otp(request):
    print(request.session.get('email'))
    try:
        user=Account.objects.get(email=request.session['email'])
    except:
        pass
    stored=request.session['OTP_Key']
    print(stored,user, type(stored))
    if request.method =='POST':
        entered=request.POST.get('otp')
        if stored==entered:
            login(request,user)
            messages.success(request, "Login successful!")
            return redirect('app:index')
        else:
            messages.warning(request, "Invalid OTP!")
            return redirect('accounts:verify-otp')
    return render(request,'evara-frontend/otp.html')



def resend_otp(request):
   print("###########################################")
   random_num=random.randint(1000,9999)
   request.session['OTP_Key']=str(random_num)
   send_mail(
   "OTP AUTHENTICATING TimeMachine",
   f"{random_num} -OTP",
   "ecomm.apps.info@gmail.com",
   [request.session['email']],
   fail_silently=False,
    )
   messages.success(request, "OTP has been resent successfully!")
   return redirect('accounts:verify-otp')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register(request):
    if request.user.is_authenticated:
        return redirect('app:index')

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['password2']
        referral_id = request.POST['referral_id']

        # Check for white spaces in username, password, and email
        if any(char.isspace() or re.match('[@#$%^@%@#%&]', char) for char in username):
            messages.error(request, "Username contains invalid characters")
        elif any(char.isspace() or re.match('[#$%^%&]', char) for char in email):
            messages.error(request, "Invalid email format")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email is Already taken")
        elif password != confirmpassword:
            messages.error(request, "Please make sure passwords match")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            if referral_id:
                try:
                    referrer = Account.objects.get(referral_id=referral_id)

                    try:
                       
                        referd_user = Wallet.objects.get(user=referrer)
                        print("referd_userrrrrrrrrrrrrrrrrrrrrrrrr",referd_user)
                      


                        # Filter instead of get_or_create to handle multiple objects
                        referd_user_transactions = WalletTransaction.objects.filter(wallet=referd_user)

                        for transaction in referd_user_transactions:
                            # Create a new transaction for each existing transaction
                            new_transaction = WalletTransaction.objects.create(
                                wallet=referd_user,
                                amount=150,
                                transaction_type="Credit",
                                transaction_detail="Got a reward From Referrals"
                            )
                            new_transaction.save()

                    except Wallet.DoesNotExist:
                        messages.error(request, 'No Wallet exists for this user.')

                    user_wallet, created = Wallet.objects.get_or_create(user=user, defaults={'balance': 0})
                    my_transaction, created = WalletTransaction.objects.get_or_create(wallet=user_wallet, defaults={'amount': 0})

                    my_transaction.amount += 100  
                    my_transaction.transaction_type = "Credit"
                    my_transaction.transaction_detail = "Got a reward From Referrals"
                    my_transaction.save()
                    

                except Account.DoesNotExist:
                    messages.error(request, 'Invalid referral code.')

            messages.success(request, "Registration successful")
            return redirect('accounts:user-login')

    return render(request, "evara-frontend/accounts/register.html")



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def user_logout(request):
    request.session.flush()
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('accounts:user-login')

def forgotpassword(request):
    return render(request,"evara-frontend/accounts/forgotpassword.html")





########################## admin ####################################



def superadmin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Invalid admin credentials!")
            return redirect('accounts:admin_login')
    return _wrapped_view





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('accounts:admin_dashboard')

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user:
            if user.is_superuser:
                login(request, user)
                messages.success(request, "Admin login successful!")
                return redirect('accounts:admin_dashboard')  # Use the named URL pattern
            messages.error(request, "Invalid admin credentials!")


    return render(request, 'evara-backend/page-account-login.html')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='accounts:admin_login')  # Use the named URL pattern
@superadmin_required
def admin_dashboard(request):

    return render(request,'evara-backend/index.html')




@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_logout(request):
    # if 'email' in request.session:
    #     del request.session['email']
    logout(request)
    messages.info(request,"Logout Successfully")
    return render(request, 'evara-backend/page-account-login.html')   











def get_order_count_by_month(start_date, end_date):
    date_count_map = {}
    current_date = start_date
    while current_date <= end_date:
        date_count_map[str(current_date.day)] = Order.objects.filter(created_at__date=current_date).count()
        current_date += timedelta(days=1)
    return date_count_map

def get_order_count_by_week(start_date, end_date):
    date_count_map = {}
    current_date = start_date
    while current_date <= end_date:
        date_count_map[str(current_date.weekday())] = Order.objects.filter(created_at__date=current_date).count()
        current_date += timedelta(days=1)
    return date_count_map

def get_order_count_by_year(start_date, end_date):
    date_count_map = {}
    current_date = start_date
    while current_date.month <= end_date.month and current_date.year <= end_date.year:
        date_count_map[str(current_date.month)] = Order.objects.filter(
            created_at__year=current_date.year, created_at__month=current_date.month
        ).count()
        current_date += timedelta(days=32)
        current_date = current_date.replace(day=1)
        
    for month, count in date_count_map.items():
        print(f'Month: {month}, Order Count: {count}')
        
    return date_count_map

def fetch_data_week(request):
    print("jjjjjjjjjjjjjj")
    today = datetime.datetime.now()
    start_date = today - timedelta(days=today.weekday())
    end_date = start_date + timedelta(days=6)
    graph_data = get_order_count_by_week(start_date, end_date)
    return JsonResponse(graph_data)


def fetch_data_month(request):
    today = datetime.datetime.now()
    print("todayllllllllll",today)
    start_date = today.replace(day=1)
    end_date = (today.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    graph_data = get_order_count_by_month(start_date, end_date)
    return JsonResponse(graph_data)


def fetch_data_year(request):
    today = datetime.datetime.now()
    start_date = today.replace(month=1, day=1)
    end_date = today.replace(month=12, day=31)
    print("ddddddddddddddddddddd",start_date, end_date)
    graph_data = get_order_count_by_year(start_date, end_date)
    for key, value in graph_data.items():
        print(f'Month: {key}, Order Count: {value}')
    
    return JsonResponse(graph_data)

