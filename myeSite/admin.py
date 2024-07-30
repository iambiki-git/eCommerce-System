from django.contrib import admin
from .models import Product, Brand, Category, Subcategory, ProductImage
from .models import Wishlist, CartSystem

 
# # Register your models here.

class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'stock_status', 'old_price', 'new_price', 'discount_price', 'brand', 'category', 'subcategory')
    list_filter = ('brand', 'category', 'subcategory')
    search_fields = ('name', 'description')
    inlines = [ProductImageInline]

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_date')
    search_fields = ('user__username', 'product__name')

class CartSystemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'size', 'brand')
    list_filter = ('user', 'product', 'size', 'brand')
    search_fields = ('user__username', 'product__name', 'size', 'brand__name')
    ordering = ('-user', 'product')








admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)


admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(CartSystem, CartSystemAdmin)
