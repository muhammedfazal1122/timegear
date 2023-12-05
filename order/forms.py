from django import forms
from .models import Order
from .models import Coupon

class OrderForm(forms.ModelForm):
  class Meta:
    model = Order
    fields = ['first_name','last_name','phone',  'address_line_1', 
               'country', 'state', 'city',  'pincode']

