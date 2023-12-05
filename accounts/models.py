from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
import uuid

# Create your models here . 

class MyAccountManager(BaseUserManager):
    def create_user(self, username, email, password=None,**extra_fields):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have a username")

        user = self.model(
            email=self.normalize_email(email), # this will neglect the casesensitive
            username=username,
            # first_name=first_name,         
            # last_name=last_name,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phonenumber = models.CharField(max_length=50)
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=50,unique=True)
    referral_id = models.UUIDField(max_length=8, default=uuid.uuid4, unique=True, null=True ,blank=True)


    # REQUIRED
    date_joined = models.DateTimeField(  auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active= models.BooleanField(default=True)
    is_superuser= models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ["username"]

    objects=MyAccountManager()

    def __str__(self) :
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self,add_label):
        return True
