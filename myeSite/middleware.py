from decimal import Decimal
from .models import CartSystem

class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            cart_items = CartSystem.objects.filter(user=request.user)
            

            subtotal = Decimal('0.00')
            discount = Decimal('0.00')
            shipping = Decimal('150.00')

            cart_item_details = []

            

            for item in cart_items:
                item_total = item.quantity * item.product.new_price
                subtotal += item_total
                

                cart_item_details.append({
                    'product': item.product,
                    'quantity': item.quantity,
                    'size' : item.size,
                    'price': item.product.new_price,
                    'total': item_total
                   
                })
               

            total = (subtotal - discount) + shipping

            request.cart_items = cart_items
            request.cart_item_details = cart_item_details
            request.cart_summary = {
                'subtotal': subtotal,
                'discount': discount,
                'shipping': shipping,
                'total': total,
            }
        else:
            request.cart_items = []
            request.cart_item_details = []
            request.cart_summary = {
                'subtotal': Decimal('0.00'),
                'discount': Decimal('0.00'),
                'shipping': Decimal('0.00'),
                'total': Decimal('0.00'),
            }
       
        response = self.get_response(request)
        return response
