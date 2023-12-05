from django.db import models
from accounts.models import Account
from order.models import Order


# Create your models here.
class AdressBook(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE,null=True, default=None)
    first_name = models.CharField(max_length=50,null=True,blank=True)
    last_name = models.CharField(max_length=50,null=True,blank=True)
    phone = models.CharField(max_length=15,default=9877655444)
    email = models.EmailField(max_length=100, default='example@example.com')
    address_line_1 = models.CharField(max_length=150,null=True,blank=True)
    address_line_2 = models.CharField(max_length=150,null=True,blank=True)
    country = models.CharField(max_length=50,null=True,blank=True)
    state = models.CharField(max_length=50,null=True,blank=True)
    city =models.CharField(max_length=50,null=True,blank=True)
    pincode = models.CharField(max_length=10,null=True,blank=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.address_line_1     



class Wallet(models.Model):
  user = models.OneToOneField(Account, on_delete=models.CASCADE)
  balance = models.IntegerField(default=0)
  is_active = models.BooleanField(default=True)

  def __str__(self):
    return self.user.username + str(self.balance)
  

class WalletTransaction(models.Model):
  TRANSACTION_TYPE_CHOICES =(
    ("CREDIT", "Credit"),
    ("DEBIT", "Debit"),
  )
  wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
  order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
  transaction_type = models.CharField(choices=TRANSACTION_TYPE_CHOICES, max_length=10)
  transaction_detail = models.CharField(max_length=50)
  amount = models.IntegerField(default=0)
  created_at = models.DateField(auto_now_add=True)

  def __str__(self):
    return self.transaction_type + str(self.wallet) + str(self.amount)

