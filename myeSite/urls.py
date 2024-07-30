from django.urls import path
from .import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name="index"),
    path('contactus/', views.contactusPage, name="contactus"),
    path('aboutus/', views.aboutusPage, name='aboutus'),
    path('login/', views.loginModule, name='login'),
    path('signup/', views.signupModule, name='signup'),
    path('subcategory/<str:subcategory_name>/', views.subcategory_details, name='product'),
    path('items-details/<int:pk>/', views.itemsDetailsPage, name='itemsDetail'),
   


    

    path('cart/', views.cart, name='cart'),
    # path('add_to_cart/', views.add_to_cart, name="add_to_cart"),

    path('wishlist-details/', views.wishlistDetail, name='wishlistdetail'),
    path('remove-from-wishlist/', views.remove_from_wishlist, name='remove_from_wishlist'),

    path('logout/', views.logoutModule, name='logoutModule'),


    # path('admin-dashboard/', views.adminBasePage, name='admin'),
]
