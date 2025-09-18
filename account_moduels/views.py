from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import login
from django.contrib import messages
from .form import MobileForm,UserRegisterForm,UserLoginForm,VerifyCodeForm,ResetPasswordForm,ForgotPasswordForm
from django.contrib.auth import authenticate
from .models import User
from django.utils.crypto import get_random_string



class LoginOrRegisterView(View):
    def get(self, request):
        context = {'form': MobileForm(), 'step': 'mobile'}
        return render(request, 'account_modules/login_or_register.html', context)

    def post(self, request):
        step = request.POST.get('step')
        mobile = request.session.get('verification_mobile')

        if step == 'mobile':
            form = MobileForm(request.POST)
            if form.is_valid():
                mobile = form.cleaned_data.get('mobile')
                request.session['verification_mobile'] = mobile
                user_exists = User.objects.filter(mobile=mobile).exists()
                if user_exists:
                    context = {'form': UserLoginForm(), 'step': 'login', 'mobile': mobile}
                    return render(request, 'account_modules/login_or_register.html', context)
                else:
                    context = {'form': UserRegisterForm(), 'step': 'register', 'mobile': mobile}
                    return render(request, 'account_modules/login_or_register.html', context)
            else:
                context = {'form': form, 'step': 'mobile'}
                return render(request, 'account_modules/login_or_register.html', context)

        elif step == 'login' and mobile:
            form = UserLoginForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=mobile, password=password)
                if user and user.check_password(password):
                    if not user.is_active:
                        code = get_random_string(5, allowed_chars='0123456789')
                        user.verification_code = code
                        user.save()
                        # send_verification_code(mobile, code)
                        return redirect(reverse_lazy('verify_code_page'))

                    login(request, user)
                    user.save()
                    return redirect('home')  # Redirect to your home page
                else:
                    form.add_error(None, 'شماره موبایل یا رمز عبور اشتباه است.')
            context = {'form': form, 'step': 'login', 'mobile': mobile}
            return render(request, 'account_modules/login_or_register.html', context)

        elif step == 'register' and mobile:
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                # --- ADDED FIELDS TO USER CREATION ---
                user = User(
                    username=data['email'],
                    email=data['email'],
                    first_name=data['first_name'],  # Add first name
                    last_name=data['last_name'],  # Add last name
                    mobile=mobile,
                    is_active=False
                )
                # --- END OF CHANGE ---
                user.set_password(data['password'])
                code = get_random_string(5, allowed_chars='0123456789')
                user.verification_code = code
                user.save()
                # send_verification_code(mobile, code)
                return redirect(reverse_lazy('verify_code_page'))
            context = {'form': form, 'step': 'register', 'mobile': mobile}
            return render(request, 'account_modules/login_or_register.html', context)

        return redirect(reverse_lazy('login_or_register_page'))


class VerifyCodeView(View):
    def get(self, request):
        # **CHANGE 2: Reading from the new session key**
        mobile = request.session.get('verification_mobile')
        if not mobile:
            return redirect(reverse_lazy('login_or_register_page'))

        form = VerifyCodeForm()
        context = {'form': form, 'mobile': mobile}
        return render(request, 'account_modules/verify_code.html', context)

    def post(self, request):
        # **CHANGE 3: Reading from the new session key**
        mobile = request.session.get('verification_mobile')
        if not mobile:
            return redirect(reverse_lazy('login_or_register_page'))

        form = VerifyCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            try:
                user = User.objects.get(mobile=mobile, verification_code=code)

                user.is_active = True
                user.verification_code = ""

                user.save()

                login(request, user, backend="account_moduels.backends.MobileBackends")

                # **CHANGE 4: Deleting the new session key**
                if 'verification_mobile' in request.session:
                    del request.session['verification_mobile']

                return redirect(reverse_lazy('home'))

            except User.DoesNotExist:
                form.add_error('code', 'کد وارد شده صحیح نمی باشد.')

        context = {'form': form, 'mobile': mobile}
        return render(request, 'account_modules/verify_code.html', context)


class ForgotPasswordView(View):
    def get(self, request):
        form = ForgotPasswordForm()
        return render(request, 'account_modules/forgot_password.html', {'form': form})

    def post(self, request):
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            mobile = form.cleaned_data.get('mobile')
            user = User.objects.filter(mobile=mobile).first()

            code = get_random_string(5, allowed_chars='0123456789')
            user.verification_code = code
            user.save()

            send_verification_code(mobile, code)
            request.session['password_reset_mobile'] = mobile

            return redirect(reverse_lazy('reset_password_page'))

        return render(request, 'account_modules/forgot_password.html', {'form': form})


class ResetPasswordView(View):
    def get(self, request):
        mobile = request.session.get('password_reset_mobile')
        if not mobile:
            return redirect(reverse_lazy('forgot_password_page'))

        context = {
            'form': VerifyCodeForm(),
            'step': 'verify_code',
            'mobile': mobile
        }
        return render(request, 'account_modules/reset_password.html', context)

    def post(self, request):
        mobile = request.session.get('password_reset_mobile')
        if not mobile:
            return redirect(reverse_lazy('forgot_password_page'))

        step = request.POST.get('step')

        if step == 'verify_code':
            form = VerifyCodeForm(request.POST)
            if form.is_valid():
                code = form.cleaned_data.get('code')
                try:
                    user = User.objects.get(mobile=mobile, verification_code=code)
                    user.verification_code = ""  # Invalidate the code
                    user.save()

                    request.session['can_reset_password'] = True
                    # Show the next step
                    context = {
                        'form': ResetPasswordForm(),
                        'step': 'set_password',
                        'mobile': mobile
                    }
                    return render(request, 'account_modules/reset_password.html', context)

                except User.DoesNotExist:
                    form.add_error('code', 'کد وارد شده صحیح نمی باشد.')

            context = {'form': form, 'step': 'verify_code', 'mobile': mobile}
            return render(request, 'account_modules/reset_password.html', context)

        elif step == 'set_password' and request.session.get('can_reset_password'):
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data.get('password')
                user = User.objects.get(mobile=mobile)
                user.set_password(password)
                user.save()

                # Clean up session
                del request.session['password_reset_mobile']
                del request.session['can_reset_password']

                messages.success(request, 'گذرواژه شما با موفقیت تغییر کرد. اکنون می‌توانید وارد شوید.')
                return redirect(reverse_lazy('login_or_register_page'))

            context = {'form': form, 'step': 'set_password', 'mobile': mobile}
            return render(request, 'account_modules/reset_password.html', context)

        return redirect(reverse_lazy('forgot_password_page'))

