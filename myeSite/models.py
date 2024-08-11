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
    
class Size(models.Model):
    name = models.CharField(max_length=50)

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
    sizes = models.ManyToManyField(Size)

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
    added_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}'s wishlist item: {self.product.name}"
    
class CartSystem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=50)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity}, Size: {self.size}, Brand: {self.brand.name})"

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=50, blank=False, null=False)
    city = models.CharField(max_length=30, null=False, blank=False)
    address = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=10, null=False, blank=False)
    shipping_option = models.CharField(max_length=100)
   
    def __str__(self):
        return f"{self.fullname} - {self.address}"
    
    

class BillingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    fullname = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.username}'s billing address: {self.fullname}, {self.city}"


