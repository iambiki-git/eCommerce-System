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
    path('delete_review/<int:pk>/', views.delete_review, name='delete_review'),

    path('changePassword/', views.ChangePassword, name="changePassword"),


    

    path('cart/', views.cart, name='cart'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),

    path('wishlist-details/', views.wishlistDetail, name='wishlistdetail'),
    path('remove-from-wishlist/', views.remove_from_wishlist, name='remove_from_wishlist'),

    path('shipping_address/', views.shipping_address, name="shipping_address"),
    # path('billingAddress/', views.billingAddress, name="billingAddress"),

    # path('payment/', views.payment, name='payment'),
    path('process_billing_info/', views.process_billing_info, name='process_billing_info'),
    path('get_shipping_address/', views.get_shipping_address, name='get_shipping_address'),
    path('payment/', views.payment, name='payment'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
    path('logout/', views.logoutModule, name='logoutModule'),


    # path('admin-dashboard/', views.adminBasePage, name='admin'),
]
