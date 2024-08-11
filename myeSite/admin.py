from django.contrib import admin
from .models import Product, Brand, Category, Subcategory, ProductImage
from .models import Wishlist, CartSystem, Size, ShippingAddress, BillingAddress

 
# # Register your models here.

class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)

class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    list_filter = ('category',)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'stock_status', 'old_price', 'new_price', 'discount_price', 'brand', 'category', 'subcategory')
    list_filter = ('brand', 'category', 'subcategory')
    search_fields = ('name', 'description')
    inlines = [ProductImageInline]

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image')

class SizeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)


class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'added_date')
    search_fields = ('user__username', 'product__name')

class CartSystemAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity', 'size', 'brand')
    list_filter = ('user', 'product', 'size', 'brand')
    search_fields = ('user__username', 'product__name', 'size', 'brand__name')
    ordering = ('-user', 'product')


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'fullname', 'city', 'address', 'contact_number', 'shipping_option')

class BillingAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','email', 'fullname', 'address', 'city', 'state', 'contact_number')

# class ShippingOptionAdmin(admin.ModelAdmin):
#     list_display = ('option_name',)




admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Size, SizeAdmin)

\


admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(CartSystem, CartSystemAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(BillingAddress, BillingAddressAdmin)
# admin.site.register(ShippingOption, ShippingOptionAdmin)
