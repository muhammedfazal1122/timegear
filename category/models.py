from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50,unique=False)
    description = models.TextField(max_length=320)
    cat_image = models.ImageField(upload_to='photos/category',blank=True) 
    soft_deleted = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    is_offer_available = models.BooleanField(default=False)
    discount = models.IntegerField( default=0)
    minimum_amount = models.IntegerField(default=100)
    end_date = models.DateField()  # Assuming you want the end date one year from today

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Category'

    def __str__(self) -> str:
        return self.category_name
    def is_expired(self):
        return self.end_date < timezone.now().date()
