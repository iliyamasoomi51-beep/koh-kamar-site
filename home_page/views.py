from django.shortcuts import render

from product_app.models import Product
from django.views.generic import ListView
def home(request):
    return render(request,'home_page/home.html')


class productlist_heder(ListView):
    model : Product
    template_name = 'header.html'
    context = {
        "products"
    }
