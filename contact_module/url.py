from . import views
from django.urls import path



urlpatterns = [

    path('contact/',views.contact_page_view, name='contact_page'),

]