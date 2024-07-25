from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .models import Items, ItemsImage, UserTable
# from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
import random
# from django.contrib.auth.decorators import login_required
from django.urls import reverse



# Create your views here.
def index(request):
    items = Items.objects.all()
    return render(request, 'myeSite/index.html', {'items':items})


def loginModule(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
    
        errors = []

        try:
            # Check if user exists
            user = UserTable.objects.filter(email=email).first()
            
            if user is not None:
                # Verify password
                if user.password == password:  # Consider hashing passwords in practice
                    # Create a session manually
                    request.session['user_id'] = user.id
                    # messages.success(request, 'Login successful!')
                    return redirect('/')  # Redirect to a home page or dashboard
                else:
                    errors.append('Wrong password.')
            else:
                errors.append('Wrong email address.')

        except Exception as e:
            errors.append(f'Error during login: {str(e)}')

        # Pass errors to the template
        return render(request, 'myeSite/loginModule.html', {'errors': errors})

    return render(request, 'myeSite/loginModule.html')



def signupModule(request):
    if request.method == 'POST':
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirm_password')

        errors = []

        # Check for password mismatch
        if password != confirmPassword:
            errors.append('Passwords do not match!')

        # Validate email and phone number uniqueness
        try:
            if UserTable.objects.filter(email=email).exists():
                errors.append('Email address already exists.')
            if UserTable.objects.filter(phone=phone).exists():
                errors.append('Phone number already exists.')
        except Exception as e:
            errors.append(f'Error checking existing records: {str(e)}')

        if errors:
            # If there are errors, pass them to the template
            return render(request, 'myeSite/signupModule.html', {'errors': errors})

        try:
            # Create user instance
            user = UserTable(
                firstname=firstname,
                lastname=lastname,
                email=email,
                phone=phone,
                password = password,
                confirmPassword = confirmPassword
            )
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
                elif 'phone' in error_message:
                    errors.append('Phone number already exists.')
                else:
                    errors.append(f'Integrity error: {error_message}')
            else:
                errors.append(f'Error: {error_message}')

            # If there are errors, pass them to the template
            return render(request, 'myeSite/signupModule.html', {'errors': errors})

    return render(request, 'myeSite/signupModule.html')


def contactusPage(request):
    return render(request, 'myeSite/contact-us.html')


def aboutusPage(request):
    return render(request, 'myeSite/about-us.html')

def tShirt(request):
    items = Items.objects.filter(category='Top Wear', sub_category='T-Shirt') 
    items_count = items.count()
    return render(request, 'myeSite/productPages/product-tShirt.html', {'items':items, 'item_count':items_count})

def itemsDetailsPage(request, pk):
    tshirt = get_object_or_404(Items, pk=pk)
    related_image = tshirt.images.all()
    return render(request, 'myeSite/productPages/items-details.html', {'tshirt':tshirt, 'related_images':related_image})


def jeansProductPage(request):
    items = Items.objects.filter(category='Bottom Wear', sub_category='Jeans') 
    items_count = items.count()
    return render(request, 'myeSite/productPages/product-jeans.html', {'items':items, 'item_count':items_count})

def shortsProductpage(request):
    items = Items.objects.filter(category='Bottom Wear', sub_category='Shorts') 
    items_count = items.count()
    return render(request, 'myeSite/productPages/product-shorts.html', {'items':items, 'item_count':items_count})

def sneakerProductPage(request):
    items = Items.objects.filter(category='Foot Wear', sub_category='Sneaker') 
    items_count = items.count()
    return render(request, 'myeSite/productPages/product-sneakers.html', {'items':items, 'item_count':items_count})

def bagProductPage(request):
    items = Items.objects.filter(category='Accessories', sub_category='Bag') 
    items_count = items.count()
    return render(request, 'myeSite/productPages/product-bag.html', {'items':items, 'item_count':items_count})

def sunglassProductPage(request):
    items = Items.objects.filter(category='Accessories', sub_category='Sunglass') 
    items_count = items.count()
    return render(request, 'myeSite/productPages/product-sunglass.html', {'items':items, 'item_count':items_count})




#cart views
def cart(request):   
    # if 'user_id' not in request.session:
    #     return redirect(reverse('login'))
    return render(request, 'myeSite/cart/cart.html')


# Admin Views
def adminBasePage(request):
    return render(request, 'myeSite/admin/base.html')


def logoutModule(request):
    try:
        # Clear the session
        request.session.flush()
        messages.success(request, 'Thanks for visiting! We hope to see you again soon.☺️')
    except Exception as e:
        messages.error(request, f'Error during logout: {str(e)}')
    
    return redirect('login')  # Redirect to the login page or home page