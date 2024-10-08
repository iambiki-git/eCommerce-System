from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .models import Product, Category, Subcategory, Wishlist, Brand, CartSystem, ShippingAddress, BillingAddress, UserOrder, Review
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
import random
from django.urls import reverse
from django.core.paginator import Paginator


# Create your views here.

from decimal import Decimal
def index(request):
    newItem = list(Product.objects.filter(isnew=True))
    random.shuffle(newItem)
    newItem=newItem[:4]

    # Filter to have only one product per subcategory in new items
    unique_new_items = {}
    for item in newItem:
        if item.subcategory not in unique_new_items:
            unique_new_items[item.subcategory] = item
    newItem = list(unique_new_items.values())[:4]  # Limit to 4 items

    #featured-products ko lagi 
    items = list(Product.objects.filter(isnew=False, is_featured=True))
    random.shuffle(items)  # Shuffle the list

    #product-categories
    category_items = Product.objects.all()
    random.shuffle(items)  # Shuffle the list

     # Filter to have only one product per subcategory in regular items
    unique_items = {}
    for cat_item in category_items:
        if cat_item.subcategory not in unique_items:
            unique_items[cat_item.subcategory] = cat_item

    cat_items = list(unique_items.values())  # No limit on regular items

    return render(request, 'myeSite/index.html', {'items':items, 'newItems':newItem, 'cat_items':cat_items})



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

def user_order_details(request):
    # Fetch all orders for the logged-in user
    user_orders = UserOrder.objects.filter(user=request.user).order_by('-id')

    # Pass the orders to the template
    context = {
        'user_orders': user_orders,
    }
    return render(request, 'myeSite/user_order_details.html', context)

def user_search_view(request):
    query = request.GET.get('search', '')
    results = []
    if query:
        results = Product.objects.filter(
            Q(search_keywords__icontains=query) | Q(name__icontains=query) | Q(description__icontains=query) | Q(code__icontains=query)
        )
    
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login')
        
        product_id = request.POST.get('productid')
        product = Product.objects.get(id = product_id)

        # Check if the product is already in the wishlist
        if Wishlist.objects.filter(user=request.user, product=product).exists():
            messages.info(request, 'This Item is already in wishlist!!!')
        else:
            Wishlist.objects.create(user=request.user, product=product)
            messages.success(request, 'Item added to wishlist!')

        return redirect(f'{request.path}?search={query}')
    
    context = {
        'results':results,
        'query':query
    }
    return render(request, 'myeSite/search_results.html', context)

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

from django.utils import timezone
def itemsDetailsPage(request, pk):   
    item = get_object_or_404(Product, pk=pk)
    related_image = item.images.all()
    product = get_object_or_404(Product, id=pk)    
    reviews = Review.objects.filter(product=product)

    sold_quantity = ProductSalesRecord.objects.filter(product=product).aggregate(total_sold=Sum('quantity_sold'))['total_sold'] or 0

    # Optionally get category_id from the product or a different source
    category_id = item.category.id if item.category else None
    # Get recommended products based on price similarity
    recommended_products = price_based_recommendation(pk, category_id=category_id)

    
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

        elif form_type == 'review-post':
            if not request.user.is_authenticated:
                return redirect('login')
            
            review_text = request.POST.get('review')
            product_id = request.POST.get('item_id')
            product = get_object_or_404(Product, id=product_id)
    
            review = Review (
                user = request.user,
                product = product,
                review_text = review_text,
                created_at = timezone.now()
            )
            review.save()
            return redirect(request.path)
        

        return redirect(request.path)
    return render(request, 'myeSite/productPages/items-details.html', {'item':item, 'related_images':related_image, 'reviews':reviews, 'recommended_products':recommended_products, 'sold_quantity':sold_quantity, 'sold_quantity': sold_quantity})

def delete_review(request, pk):
    review = get_object_or_404(Review, id=pk)
    
    if review.user == request.user:
        review.delete()
    
    return redirect(request.META.get('HTTP_REFERER', 'itemsDetail'))

#cart views
def cart(request): 
    if request.user.is_authenticated:
        cart_items = CartSystem.objects.filter(user=request.user).order_by('-id')
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
        

        shipping_address, created = ShippingAddress.objects.get_or_create(
            user=request.user,
            defaults={
                'fullname': fullname,
                'city': city,
                'address': address,
                'contact_number': contact_number,
                'shipping_option': shipping_option
            }
        )

        # If an existing address was found, update it with new data
        if not created:
            shipping_address.fullname = fullname
            shipping_address.city = city
            shipping_address.address = address
            shipping_address.contact_number = contact_number
            shipping_address.shipping_option = shipping_option
            shipping_address.save()  # Save the updated shipping address

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
    'standard': Decimal('0.00'),
    'express': Decimal('150.00'),
    'overnight': Decimal('250.00'),
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

    # Handle the case where no address is returned
    if shipping_address is None:
        return redirect('shipping_address')
    
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


def order_confirmation(request):
    return render(request, 'myeSite/order_confirmation.html')


from datetime import date
from .models import OrderItem, ProductSalesRecord
def place_order(request):
    if request.method == 'POST':
        cart_items = CartSystem.objects.filter(user=request.user)
        shipping_address = ShippingAddress.objects.filter(user=request.user).order_by('-id').first()
        billing_address = BillingAddress.objects.filter(user=request.user).order_by('-id').first()

        if not shipping_address or not billing_address:
            return redirect('cart')

        if not cart_items.exists():
            # If there are no cart items, redirect to the cart page
            return redirect('cart')
        
        # Calculate subtotal
        subtotal = sum(item.product.new_price * item.quantity for item in cart_items)

        # Get shipping charge based on the selected shipping option
        shipping_option = shipping_address.shipping_option
        shipping_charge = SHIPPING_CHARGES.get(shipping_option, Decimal('0.00'))

        # Calculate total amount including shipping cost
        total_amount = subtotal + shipping_charge

        # Fetch contact_number or use a default value if not available
        contact_number = shipping_address.contact_number if shipping_address else "9898989898"

        # Create a single UserOrder for the user
        order = UserOrder.objects.create(
            user=request.user,
            shipping_city=shipping_address.city,
            shipping_add=shipping_address.address,
            fullname_ship = shipping_address.fullname,
            shipping_option = shipping_address.shipping_option,
            billing_city=billing_address.city,
            billing_add = billing_address.address,
            fullname_bill = billing_address.fullname,
            contact_number=shipping_address.contact_number, 
            order_date=date.today(),
            total_amount=total_amount,
            status="Pending"
        )

        # Create OrderItem for each product in the cart
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                size = item.size,
                brand = item.brand,
                price=item.product.new_price  # Assuming price is stored in the Product model
            )

            # Update ProductSalesRecord for the sold product
            # sales_record, created = ProductSalesRecord.objects.get_or_create(product=item.product)
            # sales_record.total_sales += item.product.new_price * item.quantity  # Update total sales amount
            # sales_record.quantity_sold += item.quantity  # Update quantity sold
            # sales_record.save()  # Save the updated sales record
        
        # Clear the user's cart after placing the order
        cart_items.delete()  # This deletes all the cart items for the user

        if shipping_address:
            shipping_address.delete()
        if billing_address:
            billing_address.delete()

        return redirect('order_confirmation')
    return redirect('cart')



from django.contrib.auth import update_session_auth_hash
def ChangePassword(request):
    if request.method == "POST":
        new_pass = request.POST.get('new_pass')
        conf_pass = request.POST.get('confirm_new_pass')

        user = request.user

        if new_pass != conf_pass:
            messages.error(request, 'Passwords do not matched.')
            return redirect('changePassword')
    
        user.set_password(new_pass)
        user.save()
        
        update_session_auth_hash(request, user)
        messages.success(request, 'Password updated successfully.')
        return redirect('changePassword')


    return render(request, 'myeSite/changePassword.html')


# Admin Views
def adminBase(request):
    return render(request, 'myeSite/admin/base.html')

def adminLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('adminDashboard')
        else:
            messages.error(request, "Invalid Credentials!")

    return render(request, 'myeSite/admin/adminLogin.html')

def adminSignup(request):
    return render(request, 'myeSite/admin/adminSignup.html')

def adminLogout(request):
    logout(request)
    return redirect('adminLogin')


from django.db.models import Sum
def adminDashboard(request):
    
    if not request.user.is_authenticated:
        return redirect('adminLogin')

    products = Product.objects.all()
    products_count = products.count()

    users = User.objects.all()
    user_count = users.count()
    
    user_orders = UserOrder.objects.all()
    user_order_count = user_orders.count()

    total_sales = ProductSalesRecord.objects.aggregate(total_sales=Sum('total_sales'))['total_sales'] or 0

    # Retrieve product sales records
    product_sales_records = ProductSalesRecord.objects.select_related('product').all()

    context = {
        'users':users,
        'user_count':user_count,
        'products_count':products_count,
        'user_order_count':user_order_count,
        'total_sales': total_sales,
        'product_sales_records': product_sales_records,
    }
    return render(request, 'myeSite/admin/adminDashboard.html', context)

from django.contrib.auth.hashers import check_password, make_password
@login_required
def change_AdminPassword(request):
    if request.method == 'POST':
        new_password = request.POST.get('newPassword')
        confirm_password = request.POST.get('confirmPassword')

               
        # Check if new password and confirm password match
        if new_password == confirm_password:
            request.user.set_password(new_password)  # Hash and save the new password
            request.user.save()
            messages.success(request, "Password changed successfully. Please login.")
            return redirect('adminDashboard')  # Redirect to the dashboard or another page
        else:
            messages.error(request, "New passwords do not match")
            return redirect('adminDashboard')

    return render(request, 'myeSite/admin/adminDashboard.html')


def totalProductSales(request):
    # Fetch all ProductSalesRecord instances
    product_sales_records = ProductSalesRecord.objects.all()

    total_quantity_sold = sum(record.quantity_sold for record in product_sales_records)
    total_sales_amount = sum(record.total_sales for record in product_sales_records)


    context = {
        'product_sales_records': product_sales_records,
        'total_quantity_sold':total_quantity_sold,
        'total_sales_amount':total_sales_amount,
    }
    return render(request, 'myeSite/admin/totalProductSales.html', context)

def Brands(request):
    brands = Brand.objects.all()
    paginator = Paginator(brands, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    
    }

    return render(request, 'myeSite/admin/brands.html', context)

def brand_save(request):
    if request.method == 'POST':
        brand_id = request.POST.get('brand_id')
        brand_name = request.POST.get('brand_name')

        if brand_id:  # Update existing brand
            brand = get_object_or_404(Brand, id=brand_id)
            brand.name = brand_name
            brand.save()
        else:  # Add new brand
            Brand.objects.create(name=brand_name)

        return redirect('brands')
    
def delete_brand(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    if brand:
        brand.delete()
        return redirect('brands')

def category_list_view(request):
    categories = Category.objects.all()
    paginator = Paginator(categories, 5)  # This will not work
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'myeSite/admin/category.html', context)

def category_save(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category_name = request.POST.get('category_name')

        if category_id:  # Update existing brand
            category = get_object_or_404(Category, id=category_id)
            category.name = category_name
            category.save()
        else:  # Add new brand
            Category.objects.create(name=category_name)

        return redirect('category')

def delete_category(request, pk):
    category_item = get_object_or_404(Category, pk=pk)
    if category_item:
        category_item.delete()
        return redirect('category')
    
def subCategory_list_view(request):
    subcategories = Subcategory.objects.all()
    paginator = Paginator(subcategories, 5)  # This will not work
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'myeSite/admin/subCategory.html', context)
    
def subcategory_save(request):
    if request.method == 'POST':
        subcategory_id = request.POST.get('subcategory_id')
        subcategory_name = request.POST.get('subcategory_name')
        category_id = request.POST.get('category_id')
        
        category = get_object_or_404(Category, id=category_id)

        if subcategory_id:
            # Update existing subcategory
            subcategory = get_object_or_404(Subcategory, id=subcategory_id)
            subcategory.name = subcategory_name
            subcategory.category = category
            subcategory.save()
        else:
            # Add new subcategory
            Subcategory.objects.create(
                name=subcategory_name,
                category=category
            )

        return redirect('subcategory')

def subcategory_delete(request, pk):
    subcategory_item = get_object_or_404(Subcategory, pk=pk)
    # Retrieve the current page number from the query parameters
    page_number = request.GET.get('page', 1)  # Default to page 1 if 'page' is not present
    
    if subcategory_item:
        subcategory_item.delete()

        # Construct the redirect URL using reverse
        redirect_url = reverse('subcategory') + f'?page={page_number}'

        return redirect(redirect_url)
        
from .models import Size
def Products(request):
    products = Product.objects.all()
    brands = Brand.objects.all()
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    sizes = Size.objects.all()

    products = Product.objects.annotate(sold_quantity=Sum('productsalesrecord__quantity_sold'))


    paginator = Paginator(products, 4) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {
        'page_obj': page_obj,
        'brands': brands,
        'categories': categories,
        'subcategories': subcategories,
        'sizes': sizes,
    }
    return render(request, 'myeSite/admin/products.html', context)


from .models import ProductImage
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('product_code')
        search_keyword = request.POST.get('search_keyword')
        product_desc = request.POST.get('product_desc')
        stock_status = request.POST.get('stock_status')
        old_price = request.POST.get('old_price', '0.00')
        new_price = request.POST.get('new_price')
        discount_price = request.POST.get('discount_price', '0.00')
        brand_id = request.POST.get('brand')
        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory')
        isnew = request.POST.get('isnew') == 'on'
        is_featured = request.POST.get('isfeatured') == 'on'
        sizes = request.POST.getlist('sizes')
        images = request.FILES.getlist('images')
        primary_image = request.FILES.get('primary_image')

        # Fetch related brand, category, subcategory
        brand = Brand.objects.get(id=brand_id)
        category = Category.objects.get(id=category_id)
        subcategory = Subcategory.objects.get(id=subcategory_id)

         # Create a new product
        product = Product.objects.create(
            name=name,
            code = code,
            search_keywords = search_keyword,
            description=product_desc, 
            stock_status=stock_status,
            old_price=old_price,
            new_price=new_price,
            discount_price=discount_price,
            brand=brand,
            category=category,
            subcategory=subcategory,
            image=primary_image,
            isnew=isnew,
            is_featured=is_featured,
        )

        # Add sizes to the product
        for size_id in sizes:
            size = Size.objects.get(id=size_id)
            product.sizes.add(size)

        # Save product images (up to 3)
        for image in images[:2]:
            product_image = ProductImage.objects.create(product=product, image=image)

        product.save()

        # messages.success(request, "Product added successfully!")
        return redirect('products')

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    page_no = request.GET.get('page', 1)
    if product:
        product.delete()

        redirect_url = reverse('products') + f'?page={page_no}'

        return redirect(redirect_url)
    
def edit_product(request, product_id):
    products = get_object_or_404(Product, id=product_id)
    brands = Brand.objects.all()
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    sizes = Size.objects.all()

    if request.method == 'POST':
        products.name = request.POST.get('name')
        products.code = request.POST.get('code')
        products.search_keywords = request.POST.get('search_keyword')
        products.product_desc = request.POST.get('product_desc')
        products.stock_status = request.POST.get('stock_status')
        products.old_price = request.POST.get('old_price')
        products.new_price = request.POST.get('new_price')
        products.discount_price = request.POST.get('discount_price')
        products.brand_id = request.POST.get('brand')
        products.category_id = request.POST.get('category')
        products.subcategory_id = request.POST.get('subcategory')
        products.isnew = 'isnew' in request.POST
        products.is_featured = 'isfeatured' in request.POST

        # Handle primary image replacement
        primary_image = request.FILES.get('primary_image')
        if primary_image:
            products.image = primary_image
            products.save()

        # Handle additional images
        additional_images = request.FILES.getlist('images')
        if additional_images:
            # Delete existing images if you want to replace them
            products.images.all().delete()
            # Add new images
            for image in additional_images:
                ProductImage.objects.create(product=products, image=image)

        # Handle sizes
        sizes = request.POST.getlist('sizes')
        products.sizes.set(sizes)

        products.save()
        return redirect('products')  # Replace with your redirect URL

    context = {
        'products': products,
        'brands': brands,
        'categories': categories,
        'subcategories': subcategories,
        'sizes': sizes,
    }
    return render(request, 'myeSite/admin/products.html', context)

def product_search(request):
    search_pcode = request.GET.get('searchPcode')
    if search_pcode:
        products = Product.objects.filter(code=search_pcode)
        brands = Brand.objects.all()
        categories = Category.objects.all()
        subcategories = Subcategory.objects.all()
        sizes = Size.objects.all()   

        paginator = Paginator(products, 4) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

       
        context = {
            'page_obj': page_obj,
            'brands': brands,
            'categories': categories,
            'subcategories': subcategories,
            'sizes': sizes,
        } 
        return render(request, 'myeSite/admin/products.html', context)

    else:
        products = Product.objects.all() 
        brands = Brand.objects.all()
        categories = Category.objects.all()
        subcategories = Subcategory.objects.all()
        sizes = Size.objects.all()   

        paginator = Paginator(products, 4) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
           

        context = {
            'page_obj': page_obj,
            'brands': brands,
            'categories': categories,
            'subcategories': subcategories,
            'sizes': sizes,
        }

    return render(request, 'myeSite/admin/products.html', context)


def Users(request):
    # Fetch all users, excluding the admin user (is_superuser)
    users = User.objects.filter(is_superuser=False)

    # Set up pagination with 5 users per page
    paginator = Paginator(users, 7)  # Show 5 users per page.

    page_number = request.GET.get('page')  # Get the current page number from the URL
    page_obj = paginator.get_page(page_number)  # Get the users for that page

    return render(request, 'myeSite/admin/users.html', {'users':users, 'page_obj': page_obj})

from django.contrib.auth.decorators import permission_required
@permission_required('auth.delete_user', raise_exception=True)  
def DeleteUser(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_superuser:
        # Optionally, handle the case for admin users
        # Redirect or show an error message
        return redirect('users')
    
    if request.method == 'POST':
        user.delete()
        return redirect('users')
    return render(request, 'myeSite/admin/users.html', {'user': user})

def Orders(request):
    orders = UserOrder.objects.all().prefetch_related('items__product').order_by('-id')

    # Paginate the orders
    paginator = Paginator(orders, 3)  # Show 10 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'orders': page_obj,
    }
    return render(request, 'myeSite/admin/orders.html', context)

def delete_order(request, pk):
    order = get_object_or_404(UserOrder, pk=pk)
    if order:
        order.delete()
        return redirect('orders')


@permission_required('auth.change_order', raise_exception=True)
def update_order_status(request, pk):
    order = get_object_or_404(UserOrder, id=pk)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['Pending', 'Received', 'Completed', 'Cancelled']:
            order.status = new_status
            order.save()

            if new_status == "Completed":
                 # Update TotalProductSales for each product in this order
                for item in order.items.all():
                    sales_record, created = ProductSalesRecord.objects.get_or_create(product=item.product)
                    sales_record.total_sales += item.price * item.quantity  # Update total sales amount
                    sales_record.quantity_sold += item.quantity  # Update quantity sold
                    sales_record.save()  # Save the updated sales record

        return redirect('orders')  # Redirect to the orders list or any page you want

    return redirect('orders')  # Redirect back if not POST

def UserMsg(request):
    messages = ContactUs.objects.all().order_by('-created_at')
    paginator = Paginator(messages, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'myeSite/admin/userMsg.html', {'page_obj': page_obj})

def deleteMessage(request, pk):
    msg = get_object_or_404(ContactUs, pk=pk)
    msg.delete()
    return redirect('usermsg')


#price-based algorithm

def price_based_recommendation(product_id, category_id=None, threshold=0.2):
    """
    Recommend products based on price similarity.
    :param product_id: ID of the current product
    :param threshold: The percentage difference allowed between prices (default 20%)
    :return: List of recommended products
    """
    # Get the current product
    current_product = Product.objects.get(id=product_id)
    
    # Get the price of the current product
    current_price = current_product.new_price
    
   # Convert threshold and other constants to Decimal
    threshold_decimal = Decimal(str(threshold))  # Convert threshold to Decimal
    one = Decimal('1')  # Use Decimal instead of float for 1
    
    # Define a price range based on the threshold using Decimal arithmetic
    lower_bound = current_price * (one - threshold_decimal)
    upper_bound = current_price * (one + threshold_decimal)

    # Filter products by price and optionally by category
    filters = {
        'new_price__gte': lower_bound,
        'new_price__lte': upper_bound
    }

    if category_id:
        filters['category_id'] = category_id  # Filter by category if provided
    
   # Find products within the price range (excluding the current product itself)
    recommended_products = Product.objects.filter(**filters).exclude(id=product_id)

    return recommended_products


