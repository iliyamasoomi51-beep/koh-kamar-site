from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('list/', views.productlist_heder.as_view, name='about')
]

