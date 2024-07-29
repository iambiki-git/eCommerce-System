from django.db import models

# Create your models here.

class Brand(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    stock_status = models.CharField(max_length=50, default='In Stock')
    old_price = models.DecimalField(max_digits=10, decimal_places=2, default=500,  null=True, blank=True)
    new_price = models.DecimalField(max_digits=10, decimal_places=2, default=400, null=False, blank=False)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, default=100,  null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')



from django.contrib.auth.models import User 
from django.utils import timezone
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return f"{self.user.username}'s wishlist item: {self.product.name}"