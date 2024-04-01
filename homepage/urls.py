from django.urls import path
from homepage.views import login
from homepage.views import register
from homepage.views import sale,wishlist,myorders,product_detail,products,milk_items_page,soft_drink_page,sweets,fruits,vegetables,bake_items,logout_user,profile,myself,check_out,payment_done,cart_remove,plus,minus,cancle_order,delete_address,cart,show_cart

urlpatterns = [
    path('login/',login,name='Login'),
    path('deleteaddress/<int:addid>',delete_address,name='deleteaddress'),
    path('cancleorder/<int:oid>',cancle_order,name='cancleorder'),
    path('minus/<int:cid>',minus,name='minus'),
    path('plus/<int:cid>',plus,name='plus'),
    path('register/',register,name='register'),
    path('sale/',sale,name='sale'),
    path('cart/<int:cpid>',cart,name='cart'),
    path('show_cart/',show_cart,name='show_cart'),
    path('wishlist/',wishlist,name='wishlist'),
    path('myorders/',myorders,name='myorders'),
    path('product_detail/<int:pk>',product_detail.as_view(),name='product_detail'),
    path('profile/',profile,name='profile'),
    path('myself/',myself,name='myself'),
    path('products/',products,name='products'),
    path('milk_items_page/',milk_items_page,name='milk_items_page'),
    path('soft_drink_page/',soft_drink_page,name='soft_drink_page'),
    path('sweets/',sweets,name='sweets'),
    path('fruits/',fruits,name='fruits'),
    path('vegetables/',vegetables,name='vegetables'),
    path('bake_items/',bake_items,name='bake_items'),
    path('logout_user/',logout_user,name='logout_user'),
    path('check_out/',check_out,name='check_out'),
    path('payment_done/',payment_done,name='payment_done'),
    path('cart_remove/<int:pid>',cart_remove,name='cart_remove'),
]