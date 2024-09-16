from django.db import models
import datetime

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
    code = models.CharField(max_length=8, default='361SVT', blank=True, null=True)
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
    isnew = models.BooleanField(default=False)

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



class UserOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_add = models.CharField(max_length=100, default="drn")
    shipping_city = models.CharField(max_length=100, default="drn")
    shipping_option = models.CharField(max_length=100, default="standard")
    billing_add = models.CharField(max_length=100, default="brt")
    contact_number = models.CharField(max_length=14, blank=False, null=False, default="9898989898")  # Add contact_number field
    order_date = models.DateField(default=datetime.datetime.today)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


class OrderItem(models.Model):
    order = models.ForeignKey(UserOrder, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=50, default="M")
    brand = models.CharField(max_length=50, default="Gucci")

class ContactUs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15, blank=True, null=True)
    subject = models.CharField(max_length=100)
    message = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.fullname} - {self.email}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    review_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"