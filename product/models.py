from django.db import models
from category.models import Category
from django.core.validators import MinValueValidator
from brand.models import Brand
from django.urls import reverse
from datetime import datetime
from django.db.models import CheckConstraint, Q, F
# Create your models here.


class Product(models.Model):
    product_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    max_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    offer_percentage = models.IntegerField(default=65)
    images = models.ImageField( upload_to='photos/product' )
    stock = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateField( auto_now_add=True)
    modified_date = models.DateField( auto_now_add=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    product_images2 = models.ImageField(upload_to='photos/product',null=True)
    product_images3 = models.ImageField(upload_to='photos/product',null=True)
    product_images4 = models.ImageField(upload_to='photos/product',null=True)
    product_images5 = models.ImageField(upload_to='photos/product',null=True)
    quantity = models.IntegerField(default=25)
    soft_deleted = models.BooleanField(default=False)

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(max_price__gte=F('price')),
                name='check_max_price_gte_price',
            ),
        ]



    def __str__(self) :
        return self.product_name
   


class VariationManager(models.Manager):
    def colour(self):
        return super(VariationManager,self).filter(variation_category="colour",is_active=True)


variation_category_choice = [
    ('colour', 'Colour'),  # (actual value, human-readable name)
]
    
class Variation(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100,choices=variation_category_choice,default="Colour")
    is_active = models.BooleanField(default=True)
    variation_value = models.CharField(max_length=100,default="Black")
    created_date = models.DateTimeField(auto_now=True)
    stock = models.PositiveIntegerField(default=0)
    objects = VariationManager()

    def __str__(self) -> str:
        return f"{self.variation_value}"
    
    def __unicode__(self):
        return self.product




    
class ProductVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.product_name} - {self.variation.variation_value}"