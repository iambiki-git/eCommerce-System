from django.urls import path
from .import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name="index"),
    path('contactus/', views.contactusPage, name="contactus"),
    path('aboutus/', views.aboutusPage, name='aboutus'),
    path('login/', views.loginModule, name='login'),

    path('orders/', views.user_order_details, name='user_order_details'),

    path('signup/', views.signupModule, name='signup'),
    path('subcategory/<str:subcategory_name>/', views.subcategory_details, name='product'),
    path('items-details/<int:pk>/', views.itemsDetailsPage, name='itemsDetail'),
    path('delete_review/<int:pk>/', views.delete_review, name='delete_review'),

    path('changePassword/', views.ChangePassword, name="changePassword"),

    path('search/', views.user_search_view, name='search'),

    

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

    path('admin-base-page/', views.adminBase, name='adminBase'),
    path('admin-login/', views.adminLogin, name='adminLogin'),
    path('adminLogout/', views.adminLogout, name='adminLogout'),
    path('admin-signup/', views.adminSignup, name='adminSignup'),
    path('adminDashboard/', views.adminDashboard, name='adminDashboard'),

    path('adminDashboard/change-password/', views.change_AdminPassword, name='change_password'),

    path('adminDashboard/brands/', views.Brands, name='brands'),
    path('adminDashboard/brands/save/', views.brand_save, name='brand_save'),
    path('adminDashboard/brand/delete-brand/<int:pk>', views.delete_brand, name='delete_brand'),

    path('adminDashboard/category/', views.category_list_view, name='category'),
    path('adminDashboard/category/save/', views.category_save, name='category_save'),
    path('adminDashboard/category/delete-category/<int:pk>', views.delete_category, name='delete_category'),
    
    path('adminDashboard/sub-category/', views.subCategory_list_view, name='subcategory'),
    path('adminDashboard/subcategory/save/', views.subcategory_save, name='subcategory_save'),
    path('adminDashboard/subcategory/delete-subcategory/<int:pk>', views.subcategory_delete, name='subcategory_delete'),
    
    
    

    path('adminDashboard/products/', views.Products, name='products'),
    path('adminDashboard/products/add/', views.add_product, name='add_product'),
    path('adminDashboard/products/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('adminDashboard/products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('adminDashboard/products/search/', views.product_search, name='product_search'),


    path('adminDashboard/users/', views.Users, name='users'),
    path('adminDashboard/users/delete/<int:user_id>/', views.DeleteUser, name='delete_user'),
    path('adminDashboard/orders/', views.Orders, name='orders'),
    path('adminDashboard/orders/delete/<int:pk>/', views.delete_order, name='delete_order'),
    path('adminDashboard/orders/update-status/<int:pk>/', views.update_order_status, name='update_order_status'),


    path('adminDashboard/userMessage/', views.UserMsg, name='usermsg'),
    path('adminDashboard/userMessage/deleteMessage/<int:pk>', views.deleteMessage, name='deleteMessage'),

    path('adminDashboard/totalProductSales/', views.totalProductSales, name='totalProductSales'),
    

]
