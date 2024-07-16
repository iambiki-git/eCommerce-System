from django.db import models

# Create your models here.

class Items(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='items/', null=True, blank=True)



def __str__(self):
    return f"{self.name} ({self.price})"

