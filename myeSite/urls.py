from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name="index"),
    path('contactus/', views.contactusPage, name="contactus"),
    path('aboutus/', views.aboutusPage, name='aboutus'),
    path('login/', views.loginModule, name='login'),
    path('signup/', views.signupModule, name='signup'),
    path('t-shirt/', views.tShirt, name='tshirt'),
    path('items-details/<int:pk>/', views.itemsDetailsPage, name='itemsDetail'),
    path('jeans/', views.jeansProductPage, name='jeans'),
    path('shorts/', views.shortsProductpage, name='shorts'),
    path('sneakers/', views.sneakerProductPage, name="sneaker"),
    path('bag/', views.bagProductPage, name='bag'),
    path('sunglass/', views.sunglassProductPage, name='sunglass'),


    path('cart/', views.cart, name='cart'),

    path('logout/', views.logoutModule, name='logoutModule'),



    path('admin-dashboard/', views.adminBasePage, name='admin'),
]
