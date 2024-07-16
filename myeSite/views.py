from django.shortcuts import render
from .models import Items

# Create your views here.
def index(request):
    return render(request, 'myeSite/index.html')

def loginModule(request):
    return render(request, 'myeSite/loginModule.html')

def signupModule(request):
    return render(request, 'myeSite/signupModule.html')

def contactusPage(request):
    return render(request, 'myeSite/contact-us.html')


def aboutusPage(request):
    return render(request, 'myeSite/about-us.html')

def tShirt(request):
    items = Items.objects.all() 
    return render(request, 'myeSite/product-tShirt.html', {'items':items})
