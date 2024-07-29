from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .models import Product, Category, Subcategory, Wishlist
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.db import IntegrityError
import random
from django.urls import reverse


# Create your views here.

def index(request):
    return render(request, 'myeSite/index.html')
# def index(request):
#     items = Items.objects.all()
#     return render(request, 'myeSite/index.html', {'items':items})

def loginModule(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

    
        errors = []

        if user is not None:
            auth.login(request, user)
            # messages.success(request, 'Login successful!')
            return redirect('/')
        else:
            errors.append('Invalid Credentials.')
            return render(request, 'myeSite/loginModule.html', {'errors': errors})           

    return render(request, 'myeSite/loginModule.html')


def signupModule(request):
    if request.method == 'POST':
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirm_password')

        errors = []

        # Check for password mismatch
        if password1 != password2:
            errors.append('Passwords do not match!')

        # Validate email and username uniqueness
        try:
            if User.objects.filter(email=email).exists():
                errors.append('Email address already exists.')
            if User.objects.filter(username=username).exists():
                errors.append('Username already exists.')
        except Exception as e:
            errors.append(f'Error checking existing records: {str(e)}')

        if errors:
            # If there are errors, pass them to the template
            return render(request, 'myeSite/signupModule.html', {'errors': errors})

        try:
            # Create user instance
            user = User.objects.create_user(first_name=firstname, last_name = lastname, email=email, username=username, password=password1)
            user.save()

            # Add success message
            messages.success(request, 'Registration successful. Please log in.')

            # Redirect to the login page
            return redirect('login')

        except IntegrityError as e:
            error_message = str(e)
            if 'UNIQUE constraint failed' in error_message:
                if 'email' in error_message:
                    errors.append('Email address already exists.')
                elif 'username' in error_message:
                    errors.append('Username already exists.')
                else:
                    errors.append(f'Integrity error: {error_message}')
            else:
                errors.append(f'Error: {error_message}')

            # If there are errors, pass them to the template
            return render(request, 'myeSite/signupModule.html', {'errors': errors})

    return render(request, 'myeSite/signupModule.html')


def logoutModule(request):
    logout(request)
    messages.success(request, 'Thanks for visiting! We hope to see you again soon.☺️')
    return redirect('login')


def contactusPage(request):
    return render(request, 'myeSite/contact-us.html')

def aboutusPage(request):
    return render(request, 'myeSite/about-us.html')


def subcategory_details(request, subcategory_name):
    subcategory = get_object_or_404(Subcategory, name=subcategory_name)
    items = Product.objects.filter(subcategory=subcategory)
    items_count = items.count()

    if request.method =="POST": 
        #check if the user is authenticated
        if not request.user.is_authenticated:
            return redirect('login') #redirect to login page

        product_id = request.POST.get('productid')
        product = Product.objects.get(id = product_id)

        # Check if the product is already in the wishlist
        if Wishlist.objects.filter(user=request.user, product=product).exists():
            messages.info(request, 'This Item is already in wishlist!!!')
        else:
            Wishlist.objects.create(user=request.user, product=product)
            messages.success(request, 'Item added to wishlist!')

        return redirect(request.path)
    return render(request, 'myeSite/productPages/product-list.html', {'subcateogry':subcategory, 'items':items, 'item_count':items_count})


def itemsDetailsPage(request, pk):
    item = get_object_or_404(Product, pk=pk)
    related_image = item.images.all()
    return render(request, 'myeSite/productPages/items-details.html', {'item':item, 'related_images':related_image})



# #cart views
# def cart(request):   
#     # if 'user_id' not in request.session:
#     #     return redirect(reverse('login'))
#     return render(request, 'myeSite/cart_and_wishlist/cart.html')

#Wishlist

def wishlistDetail(request):
    wishlisted_items = Wishlist.objects.all()
    return render(request, 'myeSite/cart_and_wishlist/wishlist.html', {'wishlisted_items':wishlisted_items})

def add_to_wishlist(request):
    return redirect('/product/{produ}')







# # Admin Views
# def adminBasePage(request):
#     return render(request, 'myeSite/admin/base.html')


# def categoryDisplay(request,id):
    
#     subcategories = Subcategory.objects.filter(id = id).first()
#     print(subcategories)
   
#     items = Product.objects.filter(subcategory = subcategories)
#     print(items)
#     return render(request,'myeSite/productPages/products.html',{'items':items})