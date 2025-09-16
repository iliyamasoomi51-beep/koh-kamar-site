from django import forms
from .models import Contact


class ContactForm(forms.Form):
    full_name = forms.CharField(
        label= 'نام و نام خانوادگی:',
        max_length = 50,
        error_messages = {
            'riquired':'نام و نام خانوادگی حتما باید وارد شود',
            'max_lenght':'طول کارکتر نام و نام خانوادگی نباید بیش از 50 باشد'
        },
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'نام و نام خانوادگی'
        })
        )
    email = forms.EmailField(
        label = 'ایمیل:',
        widget = forms.EmailInput(attrs={
            'class':'form-control',
            'placeholder': 'ایمیل شما'
        })
        )
    phone = forms.CharField(
        label='تلفن همراه::',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'تلفن همراه'
        })
        )
    Title = forms.CharField(
        label='موضوع:',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': ' موضوع پیام'
        })
        )
    message = forms.CharField(
        label='پیام خود را بنویسید:',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'پیام خود را بنویسید:',
            'rows': '6',
            'id':'cf-message'
        })
    )
