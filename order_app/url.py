from django.urls import path


from . import  views

urlpatterns = [
    path('add-to-cart/', views.add_product_to_order, name='add_to_cart'),
]