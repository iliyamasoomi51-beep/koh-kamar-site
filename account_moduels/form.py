
from django import forms
from django.core.exceptions import ValidationError
from .models import User

class MobileForm(forms.Form):

    mobile = forms.CharField(
        label='شماره موبایل',
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'block w-full p-3 text-base outline dark:outline-none outline-1 -outline-offset-1 placeholder:text-gray-400 sm:text-sm/6 transition-all text-gray-800 dark:text-gray-100 dark:bg-gray-900 bg-slate-100 border border-transparent hover:border-slate-200 appearance-none rounded-md focus:bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 dark:focus:ring-blue-400',
            'placeholder': '09123456789'
        })
    )

class UserRegisterForm(forms.Form):
    first_name = forms.CharField(
        label='نام',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خود را وارد کنید'}),
        max_length=30
    )
    last_name = forms.CharField(
        label='نام خانوادگی',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی خود را وارد کنید'}),
        max_length=30
    )
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ایمیل خود را وارد کنید'
        })
    )
    password = forms.CharField(
        label='گذرواژه',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'گذرواژه'
        })
    )
    confirm_password = forms.CharField(
        label='تایید گذرواژه',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'تکرار گذرواژه'
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("این ایمیل قبلا استفاده شده است.")
        return email

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise ValidationError("کلمه عبور و تکرار آن مغایرت دارند")
        return confirm_password

class UserLoginForm(forms.Form):
    """
    Form for existing users to log in with their password.
    """
    password = forms.CharField(
        label='گذرواژه',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'گذرواژه خود را وارد کنید'
        })
    )

class VerifyCodeForm(forms.Form):
    code = forms.CharField(
        label='کد تایید',
        widget=forms.TextInput(attrs={'placeholder': 'کد ارسال شده را وارد کنید'}),
        max_length=5
    )

#widget=forms.TextInput(attrs={'placeholder': 'کد ارسال شده را وارد کنید'})




class ForgotPasswordForm(forms.Form):
    mobile = forms.CharField(
        label='شماره موبایل',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره موبایل خود را وارد کنید'}),
        max_length=11
    )

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if not User.objects.filter(mobile=mobile).exists():
            raise ValidationError("کاربری با این شماره موبایل یافت نشد.")
        return mobile

class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        label='گذرواژه جدید',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'گذرواژه جدید'}),
    )
    confirm_password = forms.CharField(
        label='تکرار گذرواژه جدید',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'گذرواژه جدید را تکرار کنید'}),
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise ValidationError("گذرواژه‌ها با هم مطابقت ندارند.")
        return confirm_password

