from django.db import models
from django.utils.text import slugify

# Create your models here.

class Brand(models.Model):
    brand_name = models.CharField(max_length=100,default="brandname")
    logo = models.ImageField( upload_to='photos/product' ,null=True)
    slug = models.SlugField( null=True, blank=True,default="brandname")
    soft_deleted = models.BooleanField(default=False)


    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'


    def __str__(self):
        return self.brand_name
