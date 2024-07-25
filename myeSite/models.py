from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings


# Create your models here.

class Items(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=500)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=40)
    image = models.ImageField(upload_to='items/', null=True, blank=True)
    category = models.CharField(max_length=100, default='Top Wear')
    sub_category = models.CharField(max_length=100, default='T-Shirt')
    desc = models.TextField(default="This is description.")
    brand = models.CharField(max_length=100, default="Gucci")
    stock_status = models.CharField(max_length=50, default='In Stock')


class ItemsImage(models.Model):
    items = models.ForeignKey(Items, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='items/')

class UserTable(models.Model):
    firstname = models.CharField(max_length=50, null=False)
    lastname = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=100, unique=True, null=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, unique=True, null=False)
    password = models.CharField(max_length=100, null=False)
    confirmPassword = models.CharField(max_length=100, null=False)

# def set_password(self, raw_password):
#     from django.contrib.auth.hashers import make_password
#     self.password = make_password(raw_password)

    
# class Wishlist(models.Model):
#     user = models.ForeignKey(UserTable, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

# class WishlistItem(models.Model):
#     wishlist = models.ForeignKey(Wishlist, related_name='items', on_delete=models.CASCADE)
#     item = models.ForeignKey(Items, on_delete=models.CASCADE)
#     added_at = models.DateTimeField(auto_now_add=True)