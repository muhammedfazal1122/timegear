from django.shortcuts import render
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from accounts.models import Account
from .models import AdressBook
from datetime import datetime  # Make sure to import datetime from the correct module
from product.models import Product
from django.views import View
from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
import datetime
from django.contrib import messages
from django.conf import settings
from datetime import date, datetime
import datetime
from order.models import Order
from user.models import AdressBook
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from order.models import OrderProduct
from user.models import Wallet,WalletTransaction
from django.db.models import Sum
from django.views.decorators.http import require_http_methods



def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('account:index')

    user_profile = Account.objects.get(email=request.user.email) # Get the UserProfile instance for the logged-in user

    if request.method == 'POST':
        # Handle the form submission and update the user details
        username = request.POST.get('username')
        # email = request.POST.get('email')
        email = request.POST.get('email')
        # password = request.POST.get('password')
        # Update the user profile fields with the form data
        user_profile.email = email
        # user_profile.password = password
        user_profile.username = username

        # Save the changes to the UserProfile and User models
        user_profile.save()
        messages.success(request,"updated sucesessfully")
        return redirect('app:index')  # Redirect to the user profile page after successful update
    else:
        return render(request, 'evara-frontend/edit-profile.html', {'user_profile': user_profile})








def manage_address(request):
    if not request.user.is_authenticated:
        return redirect('app:index')
    
    user = request.user
    addresses = AdressBook.objects.filter(user=user)
    default_address = addresses.filter(is_default=True).first()

    context = {
        'addresses': addresses,
        'default_address': default_address
    }
    return render(request, 'evara-frontend/manage-address.html', context)



def add_address(request):
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('account:index')
   
        address_line_1 = request.POST.get('address')
        address_line_2 = request.POST.get('address_line_2')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        phone = request.POST.get('phone')



        #Create a new shipping address instance
        address = AdressBook(user=request.user,   phone=phone, address_line_1=address_line_1, address_line_2=address_line_2, country=country, state=state, city=city, pincode=pincode)
        address.save()
        


        # Set is_default attribute of the newly added address and reset previous default
        if request.user.is_authenticated:
            AdressBook.objects.filter(user=request.user, is_default=True).update(is_default=False)
            address.is_default = True
            address.save()

        # if 'source' in request.GET and request.GET['source'] == 'checkout':
        #     # If the source is 'checkout', redirect back to the checkout page
        #     return redirect('user:checkout')  # Replace 'checkout' with your actual checkout view name

        return redirect('user:manage_address')
        
    else:
        return render(request, 'evara-frontend/add-adddres.html')
    

def delete_address(request, address_id):
    if not request.user.is_authenticated:
        return redirect('app:index')
    
    try:
        address = AdressBook.objects.get(id=address_id)
        address.delete()
    except AdressBook.DoesNotExist:
        pass

    return redirect('user:manage_address')



def edit_address(request, address_id):

    if not request.user.is_authenticated:
        return redirect('app:index')
    
    address = get_object_or_404(AdressBook, pk=address_id)

    if request.method == 'POST':
        # Handle the form submission and update the address details

        address.address_line_1 = request.POST.get('address_line_1')
 
        address.city = request.POST.get('city')
        address.state = request.POST.get('state')
        address.country = request.POST.get('country')
        address.pincode = request.POST.get('pincode')
        address.phone = request.POST.get('phone')
        address.save()

        return redirect('user:manage_address')  # Redirect to the address page after successful update

    return render(request, 'evara-frontend/edit-address.html', {'address': address})





def get_names(request):
    search = request.GET.get('search')
    
    # Check if 'search' is not None or empty
    if search:
        objs = Product.objects.filter(product_name__istartswith=search)
        payload = [{'name': obj.product_name} for obj in objs]
    else:
        payload = []

    return JsonResponse({
        'status': True,
        'payload': payload
     })





def admn_sales_report(request):
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    status_filter = int(request.GET.get('status_filter', 0))
    current_date = timezone.now().strftime("%Y-%m-%d")
    orders = []
    print(start_date,end_date,status_filter)


    if  is_valid_date(start_date) and is_valid_date(end_date) and status_filter ==  0:
    
        orders = Order.objects.all().order_by("-created_at")
        
    elif( not is_valid_date(start_date) )  and ( not is_valid_date(end_date)) and (status_filter ==  0):
        orders = filter_order_by_date( request,start_date, end_date)
    else:

        orders = filter_order_by_date_and_status( start_date, end_date, status_filter)

    context = {
        'start_date': start_date,
        'end_date': end_date,
        'status_filter': status_filter,
        'orders': orders,
        'current_date': current_date,

    }
    print(start_date,end_date,status_filter)
    return render(request, "evara-backend/sales-report.html", context)



def filter_order_by_date( request, start_date_str, end_date_str):
    start_date = convert_string_to_date(start_date_str)
    end_date = convert_string_to_date(end_date_str)

    if start_date > end_date:
        messages.warning(request, 'Start Date Must Be Less Than End Date')
        return Order.objects.all().order_by("-created_at")
    elif start_date == end_date:
        return Order.objects.filter(created_at__date=start_date).order_by("-created_at")
    else:
        return Order.objects.filter(created_at__date__range=(start_date, end_date)).order_by("-created_at")

def filter_order_by_date_and_status( start_date_str, end_date_str, status_filter):
    if not start_date_str or start_date_str == 'null' or not end_date_str or end_date_str == 'null':
        return filter_order_by_status(status_filter)

    start_date = convert_string_to_date(start_date_str)
    end_date = convert_string_to_date(end_date_str)

    if start_date == end_date:
        
        status = get_order_status_by_value(status_filter)
        return Order.objects.filter(created_at__date=start_date, status=status).order_by("-created_at") 
    else:
        status = get_order_status_by_value(status_filter)
        return Order.objects.filter(created_at__date__range=(start_date, end_date), status=status).order_by("-created_at") 

def filter_order_by_status(status_filter):
    status = get_order_status_by_value(status_filter)

    return Order.objects.filter(status=status).order_by("-created_at") 

def get_order_status_by_value(status_filter):
    # Implement your logic to map status_filter values to actual order statuses
    # Example: 
    if status_filter == 1:                    
        return "Pending"
    elif status_filter == 2:
        return "Shipped"
    elif status_filter == 3:
        return "Deliverd"
    elif status_filter == 4:
        return "Cancelled"
    elif status_filter == 5:
        return "Returned"
    # Add more mappings as needed

def convert_string_to_date(date_str):
    if not date_str or date_str == 'null':
        return date.today()
    return datetime.strptime(date_str, '%Y-%m-%d').date()


def is_valid_date(date_str):
    if not date_str or date_str == 'null':
        return True
    try:
        # Use the full module path for strptime
        datetime.strptime(date_str, '%Y-%m-%d')
        return False
    except ValueError:
        return True




def get_weekly_sales():
    end_date = timezone.now()
    start_date = end_date - timezone.timedelta(days=7)

    return OrderProduct.objects.filter(
        order__created_at__range=(start_date, end_date)
    ).values('product__product_name').annotate(weekly_sales=Sum('quantity'))



def get_monthly_sales():
    end_date = timezone.now()
    start_date = end_date - timezone.timedelta(days=30)

    return OrderProduct.objects.filter(
        order__created_at__range=(start_date, end_date)
    ).values('product__product_name').annotate(monthly_sales=Sum('quantity'))



def get_yearly_sales():
    end_date = timezone.now()
    start_date = end_date - timezone.timedelta(days=365)

    return OrderProduct.objects.filter(
        order__created_at__range=(start_date, end_date)
    ).values('product__product_name').annotate(yearly_sales=Sum('quantity'))



def sales_report(request):
    weekly_sales_data = list(get_weekly_sales().values('product__product_name','weekly_sales'))  ## Convert QuerySet to a list of dictionaries
    monthly_sales_data = list(get_monthly_sales().values('product__product_name','monthly_sales'))
    yearly_sales_data = list(get_yearly_sales().values('product__product_name','yearly_sales'))
    sales_data = {
        'weekly_sales': weekly_sales_data,
        'monthly_sales': monthly_sales_data,
        'yearly_sales': yearly_sales_data,
    }
    return JsonResponse(sales_data, safe=False)


#------------------------------------------------WALLET-------------------------------------------------------------------------#


def my_wallet(request):
    current_user = request.user
    total_wallet_balance = 0
    
    try:
        wallet = Wallet.objects.get(user=current_user)
    except Wallet.DoesNotExist:
        # Handle the case where the user doesn't have a wallet
        messages.warning(request, 'You do not have a wallet yet. Creating a new wallet.')
        wallet = Wallet.objects.create(user=current_user, balance=0)

    wallet_transactions = WalletTransaction.objects.filter(wallet=wallet)
    increment_val = sum(transaction.amount for transaction in wallet_transactions if transaction.transaction_type=="Credit")
    decement_val = sum(transaction.amount for transaction in wallet_transactions if transaction.transaction_type=="Debit")
    print(increment_val,decement_val)
    total_wallet_balance = increment_val - decement_val
   
    wallet.balance = total_wallet_balance
    wallet.save()

    context = {
        "wallet_transactions": wallet_transactions,
        "wallet": wallet,
        "total_wallet_balance": total_wallet_balance,
    }
    return render(request, "evara-frontend/my_wallet.html", context)






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
    while current_date.month <= end_date.month:
        date_count_map[str(current_date.month)] = Order.objects.filter(
            created_at__year=current_date.year, created_at__month=current_date.month
        ).count()
        current_date = current_date.replace(month=current_date.month + 1)
    return date_count_map

def fetch_data_month(request):
    today = timezone.now().date()
    start_date = today.replace(day=1)
    end_date = (today.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    graph_data = get_order_count_by_month(start_date, end_date)
    return JsonResponse(graph_data)

def fetch_data_week(request):
    today = timezone.now().date()
    start_date = today - timedelta(days=today.weekday())
    end_date = start_date + timedelta(days=6)
    graph_data = get_order_count_by_week(start_date, end_date)
    return JsonResponse(graph_data)

def fetch_data_year(request):
    today = timezone.now().date()
    start_date = today.replace(month=1, day=1)
    end_date = today.replace(month=12, day=31)
    graph_data = get_order_count_by_year(start_date, end_date)
    return JsonResponse(graph_data)




def get_names(request):
    search = request.GET.get('search')
    
    # Check if 'search' is not None or empty
    if search:
        objs = Product.objects.filter(product_name__istartswith=search)
        payload = [{'name': obj.product_name} for obj in objs]
    else:
        payload = []

    return JsonResponse({
        'status': True,
        'payload': payload
     })
