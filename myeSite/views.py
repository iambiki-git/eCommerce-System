from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .models import Product, Category, Subcategory, Wishlist, Brand, CartSystem, ShippingAddress, BillingAddress, UserOrder
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
import random
from django.urls import reverse


# Create your views here.

from decimal import Decimal
def index(request):
    newItem = list(Product.objects.filter(isnew=True))
    random.shuffle(newItem)
    newItem=newItem[:4]
    items = list(Product.objects.all())
    random.shuffle(items)  # Shuffle the list
    return render(request, 'myeSite/index.html', {'items':items, 'newItems':newItem})

# def index(request):
#     items = Items.objects.all()
#     return render(request, 'myeSite/index.html', {'items':items})

def loginModule(request):
    if not request.user.is_authenticated:
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
    else:
        return redirect('/')


def signupModule(request):
    if not request.user.is_authenticated:
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
    else:
        return redirect('/')


def logoutModule(request):
    logout(request)
    messages.success(request, 'Thanks for visiting! We hope to see you again soon.☺️')
    return redirect('login')

from .models import ContactUs
def contactusPage(request):
    if request.method == "POST":
        fullname = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

         # Assuming the user is logged in, you can assign the user, otherwise set it to None.
        user = request.user if request.user.is_authenticated else None

        # Save the form data to the ContactUs model
        contact_message = ContactUs.objects.create(
            user = user,
            fullname = fullname,
            email = email,
            phone = phone,
            subject = subject,
            message = message
        )

        messages.success(request, "Thank you for reaching out to us! We will get back to you soon.")

        return redirect('contactus')
     
    return render(request, 'myeSite/contact-us.html')

def aboutusPage(request):
    return render(request, 'myeSite/about-us.html')

from django.db.models import Q
def subcategory_details(request, subcategory_name):
    subcategory = get_object_or_404(Subcategory, name=subcategory_name)
    items = Product.objects.filter(subcategory=subcategory) 
    brand = Brand.objects.all()
    

     # Process filters
    selected_brands = request.GET.getlist('brands')
    selected_price_ranges = request.GET.getlist('price')

    # Filter by brand
    if selected_brands:
        items = items.filter(brand__id__in=selected_brands)

      # Filter by price ranges
    if selected_price_ranges:
        price_filters = []
        if '1' in selected_price_ranges:
            price_filters.append(Q(new_price__gte=300, new_price__lte=1999))
        if '2' in selected_price_ranges:
            price_filters.append(Q(new_price__gte=1999, new_price__lte=5999))
        if '3' in selected_price_ranges:
            price_filters.append(Q(new_price__gte=5999, new_price__lte=15000))

        if price_filters:
            items = items.filter(Q(*price_filters))

    

    items_count = items.count()

    if request.method =="POST": 
        action = request.POST.get('action')
        if action == 'wishlist':
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
        elif action == "sort":
            # Sorting logic
            sort_by = request.POST.get('services')
            if sort_by == 'lowtohighprice':
                items = items.order_by('new_price')
            elif sort_by == 'hightolowprice':
                items = items.order_by('-new_price')

    return render(request, 'myeSite/productPages/product-list.html', {
        'subcateogry':subcategory, 
        'items':items, 
        'item_count':items_count, 
        'brands':brand
    })

def itemsDetailsPage(request, pk):   
    item = get_object_or_404(Product, pk=pk)
    related_image = item.images.all()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Login Required!')
            return redirect(reverse('login'))
        
        form_type = request.POST.get('form_type')
        if form_type == 'add_to_cart':
            product_id = request.POST.get('item_id') 
            size = request.POST.get('size')
            brand_id = request.POST.get('brand_id')
            quantity = int(request.POST.get('quantity', 1))
             
            if not size:
                messages.error(request, 'Please Select Size.')
                return redirect(request.path)

            product = get_object_or_404(Product, id=product_id)
            brand = get_object_or_404(Brand, id=brand_id)

            # Check if the item is already in the cart
            cart_item, created = CartSystem.objects.get_or_create(
                user=request.user,
                product=product,
                size=size,
                brand=brand
            )
            if not created:
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, 'Item quantity updated in cart!')
            else:
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, 'Item added to cart!')
        elif form_type == 'add_to_wishlist':
            if not request.user.is_authenticated:
                return redirect('login')
            
            product_id = request.POST.get('item_id')
            product = Product.objects.get(id = product_id)

            # Check if the item is already in the wishlist
            wishlist_item, created = Wishlist.objects.get_or_create(
                user=request.user,
                product=product
            )
            if not created:
                messages.info(request, 'Item is already in your wishlist!')
            else:
                messages.success(request, 'Item added to wishlist!')

        return redirect(request.path)
    return render(request, 'myeSite/productPages/items-details.html', {'item':item, 'related_images':related_image})



#cart views
def cart(request): 
    if request.user.is_authenticated:
        cart_items = CartSystem.objects.filter(user=request.user)
        for item in cart_items:
            item.total_price = item.quantity * item.product.new_price
    else:
        cart_items = []
        return redirect('login')

    context = {
        'cart_items': cart_items,
    }
    return render(request, 'myeSite/cart_and_wishlist/cart.html', context)


#Wishlist

def wishlistDetail(request):
    user = request.user
    wishlisted_items = Wishlist.objects.filter(user=user)
    return render(request, 'myeSite/cart_and_wishlist/wishlist.html', {'wishlisted_items':wishlisted_items})


def remove_from_wishlist(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = get_object_or_404(Wishlist, id=item_id)
        item.delete()
        return redirect('wishlistdetail')
    return HttpResponse(status=405)


def remove_from_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = get_object_or_404(CartSystem, id=item_id, user=request.user)
        item.delete()
        return redirect('cart')
    return HttpResponse(status=405)

def shipping_address(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        city = request.POST.get('shippingAvailableCity')
        address = request.POST.get('address')
        contact_number = request.POST.get('phone')
        shipping_option = request.POST.get('shippingOptions')
        

        shipping_address = ShippingAddress.objects.create(
            user=request.user,
            fullname=fullname,
            city=city,
            address=address,
            contact_number=contact_number,
            shipping_option=shipping_option
        )

        return redirect('process_billing_info')
    return render(request, 'myeSite/shippingAddress/shippingAddress.html')

from django.http import JsonResponse
def get_shipping_address(request):
    # Assuming there is only one shipping address per user
    shipping_address = ShippingAddress.objects.filter(user=request.user).first()

    if shipping_address:
        data = {
            'fullname': shipping_address.fullname,
            'address': shipping_address.address,
            'city': shipping_address.city,
            'contact_number': shipping_address.contact_number
        }
        return JsonResponse(data)
    else:
        return JsonResponse({}, status=404)


def process_billing_info(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        fullname = request.POST.get('billingFullName')
        address = request.POST.get('billingAddress')
        city = request.POST.get('billingCity')
        state = request.POST.get('state')
        contact_number = request.POST.get('billingPhone')

        # Create or update the billing address
        BillingAddress.objects.update_or_create(
            user=request.user,
            defaults={
                'email': email,
                'fullname': fullname,
                'address': address,
                'city': city,
                'state': state,
                'contact_number': contact_number
            }
        )

        # Redirect to the payment page
        return redirect('payment')  

    return render(request, 'myeSite/shippingAddress/billingAddress.html')


SHIPPING_CHARGES = {
    'standard': 0.00,
    'express': 150.00,
    'overnight': 250.00,
}

def payment(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if the user is not authenticated
    
    # Retrieve the user's shipping address
    try:
        shipping_address = ShippingAddress.objects.get(user=request.user)
    except ShippingAddress.DoesNotExist:
        # Handle the case where no shipping address exists
        return redirect('shipping_address')  # Redirect to a page where the user can add a shipping address

    # Get the shipping charge based on the selected shipping option
    shipping_charge = SHIPPING_CHARGES.get(shipping_address.shipping_option, 0)

    subtotal = request.cart_summary['subtotal']
    total_amt = subtotal + Decimal(shipping_charge)

    # Pass the shipping address and charge to the template
    context = {
        'shipping_address': shipping_address,
        'shipping_charge': shipping_charge,
        'subtotal': subtotal,
        'total_amount':total_amt,
    }
    return render(request, 'myeSite/payment.html', context)


# # Admin Views
# def adminBasePage(request):
#     return render(request, 'myeSite/admin/base.html')

def order_confirmation(request):
    return render(request, 'myeSite/order_confirmation.html')


from datetime import date
def place_order(request):
    if request.method == 'POST':
        cart_items = CartSystem.objects.filter(user=request.user)
        shipping_address = ShippingAddress.objects.filter(user=request.user).first()
        billing_address = BillingAddress.objects.filter(user=request.user).first()

        if not shipping_address or not billing_address:
            return redirect('cart')

        if not cart_items.exists():
            # If there are no cart items, redirect to the cart page
            return redirect('cart')
        
        # Create an order for each item in the cart
        for item in cart_items:
            UserOrder.objects.create(
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                price=item.product.new_price,  # Assuming price is stored in the Product model
                size=item.size,
                brand=item.brand,
                shipping_add= shipping_address,
                billing_add= billing_address,
                order_date=date.today()
            )
        
        # Clear the user's cart after placing the order
        cart_items.delete()  # This deletes all the cart items for the user
        if shipping_address:
            shipping_address.delete()
        if billing_address:
            billing_address.delete()

        return redirect('order_confirmation')
    return redirect('cart')



# def product_list(request):
#     products = Product.objects.all()
#     brands = Brand.objects.all()

#     # Get the filters from the request
#     selected_brands = request.GET.getlist('brands')
#     selected_price_ranges = request.GET.getlist('price')

#     # Filter by brand
#     if selected_brands:
#         products = products.filter(brand__id__in=selected_brands)
    
#     # Filter by price ranges
#     if selected_price_ranges:
#         price_filters = []
#         if '1' in selected_price_ranges:
#             price_filters.append({'price__gte': 300, 'price__lte': 1999})
#         if '2' in selected_price_ranges:
#             price_filters.append({'price__gte': 1999, 'price__lte': 5999})
#         if '3' in selected_price_ranges:
#             price_filters.append({'price__gte': 5999, 'price__lte': 15000})


#         from django.db.models import Q
#         if price_filters:
#             products = products.filter(Q(**price_filters[0]) | Q(**price_filters[1]) | Q(**price_filters[2]))
        
#     context = {
#         'products': products,
#         'brands': brands,
#     }
#     return render(request, 'product_list.html', context)
