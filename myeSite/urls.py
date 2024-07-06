from django.urls import path
from .import views

urlpatterns = [
    path('', views.main, name="main"),
    path('login/', views.loginModule, name='login'),
    path('signup/', views.signupModule, name='signup'),
    path('fashionPage/', views.fashionPage, name='fashionPage'),
]
