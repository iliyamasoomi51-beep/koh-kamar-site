
from . import views
from django.urls import path



urlpatterns = [

    path('auth/',views.LoginOrRegisterView.as_view(), name='login_or_register_page'),


    path('verify/',views.VerifyCodeView.as_view(), name='verify_code_page'),

    path('password/forgot/',views.ForgotPasswordView.as_view(), name='forgot_password_page'),

    path('password/reset/',views.ResetPasswordView.as_view(), name='reset_password_page'),



    ]