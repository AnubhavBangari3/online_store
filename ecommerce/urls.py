from django.urls import path
from . views import *
urlpatterns=[
    
    path('cart/',cart,name="cart"),
    path('',store,name="store"),
    path('checkout',checkout,name="checkout"),
    path('update_item',updateItem,name="update_item"),
    path('process_order',processOrder,name="process_order"),
    path('product/<int:id>',product,name="product"),
    path('search',search,name="search"),
    path('login_view',login_view,name="login"),
    path('logout_view',logout_view,name="logout"),
    path('register',register,name="register"),
    path('contact',contact,name="contact")
]