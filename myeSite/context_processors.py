from .models import Category, Wishlist

def categories_processor(request):
    categories = Category.objects.all().prefetch_related('subcategories')
    return {'categories': categories}

def wishlist_item_count(request):
    if request.user.is_authenticated:
        wishlist_item_count = Wishlist.objects.filter(user=request.user).count()
    else:
        wishlist_item_count = 0
    return {'wishlist_item_count': wishlist_item_count}
