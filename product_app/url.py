from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [

    path('categories/', views.category_list, name='category_list'),


    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),


    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),

    # Optional: A URL for the list of all products (if needed)
    path('Shop', views.product_list, name='product_list'),
]