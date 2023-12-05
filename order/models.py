from django.db import models
from accounts.models import *
from category.models import *
from product.models import *
from cart.models import *

# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    discount = models.FloatField(default=0,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.payment_id





class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Cancelled', 'Cancelled'),
        ('Delivered', 'Delivered'),
        ('Returned', 'Returned'),
    )


    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=150)
    address_line_1 = models.CharField(max_length=150)
    address_line_2 = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    country = models.CharField(max_length=150)
    pincode = models.CharField(max_length=10)
    order_total = models.FloatField()
    tax = models.FloatField(null=True)
    status = models.CharField(max_length=10, choices=STATUS, default='Pending')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total = models.DecimalField(max_digits=10, decimal_places=2) 
    cancellation_reason = models.CharField(max_length=150,default="Damaged Product")




    

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    
    def full_address(self):
        return f"{self.address_line_1} {self.address_line_2}"
    
    # def __str__(self):
    #     return f'{self.order_total}'
    



class OrderProduct(models.Model):
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_price = models.FloatField()
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_ordered = models.BooleanField(default=False)
    # color = models.ForeignKey(Variation, on_delete=models.CASCADE, related_name='color_variation', max_length=50)


    @property
    def get_total(self):
        total = self.product_price * self.quantity
        return total
    
 


class Coupon(models.Model):
    coupon_code = models.CharField(max_length=20, unique=True, null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_amount = models.IntegerField(default=1000)
    valid_to = models.DateField()


    def Is_Redeemed_By_User_New(self, request, user):
        coupon_code = request.POST.get("couponCode")

        # Assuming there is a Coupon model with a field named 'coupon_code'
        coupon = Coupon.objects.get(coupon_code=coupon_code)

        redeemed_details = Coupon_Redeemed_Details.objects.filter(coupon=coupon, user=user)

        return redeemed_details.exists()


class Coupon_Redeemed_Details(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_redeemed = models.BooleanField(default=False)
