from django.urls import path
from . import  views
urlpatterns = [
    path('test', views.mlm, name='test'),
    path('add-to-cart/', views.add_product_to_order, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_product_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('checkout/', views.checkout_page, name='checkout_page'),
    path('checkout/update-address/', views.update_address, name='update_address'),
    path('request_payment/', views.request_payment, name='request_payment'),
    path('verify_payment/', views.verify_payment, name='verify_payment'),
]