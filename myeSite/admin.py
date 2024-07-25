from django.contrib import admin
from .models import Items, ItemsImage, UserTable

# Register your models here.
class ItemImageInline(admin.TabularInline):
    model = ItemsImage
    extra = 1

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'sub_category')
    inlines = [ItemImageInline]

  



class UserAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'email')


admin.site.register(Items, ItemAdmin)
admin.site.register(UserTable, UserAdmin)
