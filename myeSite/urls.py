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
   


    

    # path('cart/', views.cart, name='cart'),
    path('wishlist-details/', views.wishlistDetail, name='wishlistdetail'),
    path('add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),

    path('logout/', views.logoutModule, name='logoutModule'),


    # path('admin-dashboard/', views.adminBasePage, name='admin'),
]
