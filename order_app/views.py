from django.http import HttpRequest, JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import OrderDetail, Product, Order, User
from .forms import AddressForm
import json
import requests
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Order, OrderDetail
from product_app.models import Product  # برای دسترسی به مدل محصول
from django.db.models import F
from datetime import datetime
def mlm(request):
    return render(request, "cart/mlm.html")

# def add_product_to_order(request: HttpRequest):
#
#
#     if request.method != 'POST':
#
#         return JsonResponse({'status': 'invalid_method', 'text': 'متد درخواست نامعتبر است'})
#
#     try:
#         product_id = int(request.POST.get('product_id'))
#         count = int(request.POST.get('count'))
#         print(f"3. Received data: product_id={product_id}, count={count}")
#     except (ValueError, TypeError):
#
#         return JsonResponse({
#             'status': 'invalid_input',
#             'text': 'اطلاعات ارسالی نامعتبر است',
#             'confirm_button_text': 'چشم',
#             'icon': 'error'
#         })
#
#     if count < 1:
#
#         return JsonResponse({
#             'status': 'invalid_count',
#             'text': 'مقدار وارد شده معتبر نیست',
#             'confirm_button_text': 'چشم',
#             'icon': 'warning'
#         })
#
#     if not request.user.is_authenticated:
#
#         return JsonResponse({
#             'status': 'not_logged_in',
#             'text': 'برای افزودن به سبدخرید ابتدا باید وارد سایت شوید',
#             'confirm_button_text': 'ورود به سایت',
#             'confirm_button_url': reverse_lazy('login_or_register_page'),  # تولید URL برای لاگین
#             'icon': 'error'
#         })
#
#
#     product = Product.objects.filter(id=product_id, available=True).first()
#     if product is None:
#
#         return JsonResponse({
#             'status': 'not_found',
#             'text': 'محصول مورد نظر یافت نشد',
#             'confirm_button_text': 'چشم چک میکنم',
#             'icon': 'error'
#         })
#
#
#     current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
#     order_detail, detail_created = current_order.orderdetails_set.get_or_create(
#         product_id=product_id,
#         defaults={'count': count}
#     )
#
#     if not detail_created:
#
#         order_detail.count += count
#         order_detail.save()
#
#
#     return JsonResponse({
#         'status': 'success',
#         'text': 'محصول مورد نظر با موفقیت به سبد خرید شما اضافه شد',
#         'confirm_button_text': 'باشه ممنونم',
#         'icon': 'success'
#     })
@login_required
def add_product_to_order(request: HttpRequest):
    if request.method != 'POST':
        return JsonResponse({'status': 'invalid_method', 'text': 'متد درخواست نامعتبر است'})

    try:
        product_id = int(request.POST.get('product_id'))
        count = int(request.POST.get('count'))
    except (ValueError, TypeError):
        return JsonResponse({
            'status': 'invalid_input',
            'text': 'اطلاعات ارسالی نامعتبر است',
            'confirm_button_text': 'چشم',
            'icon': 'error'
        })

    if count < 1:
        return JsonResponse({
            'status': 'invalid_count',
            'text': 'مقدار وارد شده معتبر نیست',
            'confirm_button_text': 'چشم',
            'icon': 'warning'
        })

    product = get_object_or_404(Product, id=product_id, available=True)

    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)

    order_detail, detail_created = current_order.orderdetails_set.get_or_create(
        product_id=product_id,
        defaults={'count': count, 'final_price': product.price}  # <-- قیمت محصول را اینجا اضافه کردیم
    )

    if not detail_created:
        order_detail.count += count
        order_detail.final_price = product.price  # <-- این خط را برای آپدیت قیمت اضافه کردیم
        order_detail.save()

    return JsonResponse({
        'status': 'success',
        'text': 'محصول مورد نظر با موفقیت به سبد خرید شما اضافه شد',
        'confirm_button_text': 'باشه ممنونم',
        'icon': 'success'
    })
@login_required
def cart_detail(request):
    # سبد خرید موقت (is_paid=False) کاربر را پیدا می‌کند
    cart, created = Order.objects.get_or_create(user=request.user, is_paid=False)

    # برای نمایش، از OrderDetailهای مرتبط استفاده می‌کنیم
    context = {
        'cart': cart.orderdetails_set.all(),
        'total_price': cart.calculate_total_price()  # حالا این تابع همیشه یک عدد برمی‌گرداند
    }

    return render(request, 'cart/cart_detail.html', context)
@login_required
def add_product_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # سبد خرید موقت کاربر را پیدا یا ایجاد می‌کند
    user_cart, created = Order.objects.get_or_create(user=request.user, is_paid=False)

    # ابتدا بررسی می‌کنیم که آیا این محصول از قبل در سبد هست یا نه
    order_item = OrderDetail.objects.filter(order=user_cart, product=product).first()

    if order_item:
        # اگر آیتم از قبل وجود داشت، فقط تعداد و قیمت نهایی رو آپدیت می‌کنیم
        order_item.count += 1
        order_item.final_price = product.price
        order_item.save()
    else:
        # اگر آیتم جدید بود، یک OrderDetail جدید می‌سازیم
        OrderDetail.objects.create(
            order=user_cart,
            product=product,
            final_price=product.price,
            count=1
        )

    return redirect('cart_detail')
@login_required
def remove_from_cart(request, product_id):
        # سبد خرید موقت کاربر را پیدا می‌کند
        user_cart = get_object_or_404(Order, user=request.user, is_paid=False)

        # آیتم مورد نظر برای حذف را پیدا می‌کند
        order_item = get_object_or_404(OrderDetail, order=user_cart, product__id=product_id)

        # اگر تعداد محصول بیشتر از یک باشد، یکی کم می‌کند
        if order_item.count > 1:
            order_item.count -= 1
            order_item.save()
        else:
            # اگر تعداد یک بود، کل آیتم را حذف می‌کند
            order_item.delete()

        return redirect('cart_detail')
@login_required
def clear_cart(request):
    user_cart = get_object_or_404(Order, user=request.user, is_paid=False)
    user_cart.orderdetails_set.all().delete()

    return redirect('cart_detail')
@login_required
def checkout_page(request):
    cart, created = Order.objects.get_or_create(user=request.user, is_paid=False)
    user_info = {
        'address_org': request.user.address_org,
        # ...
    }

    # فرم را به قالب می‌فرستیم
    address_form = AddressForm()

    context = {
        'cart': cart.orderdetails_set.all(),
        'total_price': cart.calculate_total_price(),
        'user_info': user_info,
        'address_form': address_form  # فرم را به context اضافه می‌کنیم
    }
    return render(request, 'cart/checkout.html', context)


@login_required
def update_address(request):
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            combined_address = address_form.get_combined_address()
            request.user.address_org = combined_address
            request.user.save()

            return redirect('checkout_page')

    return redirect('checkout_page')

ZP_API_REQUEST = ""
ZP_API_VERIFY = ""
ZP_API_STARTPAY = ""

amount = 1000
description = ""
phone = 'YOUR_PHONE_NUMBER'


@login_required
def request_payment(request):
    try:
        current_order = get_object_or_404(Order, is_paid=False, user_id=request.user.id)

        # استفاده از تابع بهینه شده calculate_total_price از مدل Order
        total_price_toman = current_order.calculate_total_price()

        if total_price_toman == 0:
            return redirect(reverse('user-basket'))  # اگر سبد خرید خالی بود، کاربر را برمی‌گرداند

        # CallBackURL باید به تابع verify_payment اشاره کند
        CallbackURL = request.build_absolute_uri(reverse('verify_payment'))

        req_data = {
            "MerchantID": settings.MERCHANT,
            "Amount": total_price_toman,  # قیمت به تومان
            "Description": f"پرداخت سفارش شماره {current_order.id}",
            "CallbackURL": CallbackURL,
        }

        req_headers = {"accept": "application/json", "content-type": "application/json"}
        response = requests.post(url=ZP_API_REQUEST, data=json.dumps(req_data), headers=req_headers)
        response_data = response.json()

        if response.status_code == 200 and 'data' in response_data:
            authority = response_data['data'].get('authority')
            if authority:
                # ذخیره Authority برای استفاده در مرحله بعد
                request.session['authority'] = authority

                return redirect(f"{ZP_API_STARTPAY}{authority}")

        errors = response_data.get('errors', {})
        e_code = errors.get('code', 'Unknown code')
        e_message = errors.get('message', 'Unknown message')
        return HttpResponse(f'خطا در درخواست پرداخت: {e_code} - {e_message}')

    except Exception as e:
        return HttpResponse(f'خطای غیرمنتظره: {str(e)}')


@login_required
def verify_payment(request):
    current_order = get_object_or_404(Order, is_paid=False, user_id=request.user.id)
    total_price_toman = current_order.calculate_total_price()

    t_authority = request.GET.get('Authority')
    if request.GET.get('Status') == 'OK' and t_authority:
        req_headers = {"accept": "application/json", "content-type": "application/json"}
        req_data = {
            "MerchantID": settings.MERCHANT,
            "Amount": total_price_toman,
            "Authority": t_authority,
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_headers)

        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                # پرداخت با موفقیت انجام شد، حالا موجودی محصولات را کم می‌کنیم
                for item in current_order.orderdetails_set.all():
                    # با استفاده از F()، موجودی را به صورت اتمیک و امن کم می‌کنیم
                    Product.objects.filter(id=item.product.id).update(stock=F('stock') - item.count)

                # نهایی کردن سفارش
                current_order.is_paid = True
                current_order.payment_date = datetime.now()
                current_order.save()

                ref_str = req.json()['data']['ref_id']

                return render(request, 'order_module/payment_result.html',
                              {'success': f'تراکنش شما با کد پیگیری {ref_str} با موفقیت انجام شد.'})
            elif t_status == 101:
                return render(request, 'order_module/payment_result.html', {'info': 'این تراکنش قبلا ثبت شده است.'})
            else:
                return render(request, 'order_module/payment_result.html',
                              {'error': f'خطا در تایید تراکنش. کد: {t_status}'})
        else:
            e_message = req.json()['errors']['message']
            return render(request, 'order_module/payment_result.html', {'error': e_message})
    else:
        return render(request, 'order_module/payment_result.html',
                      {'error': 'پرداخت با خطا مواجه شد یا توسط کاربر لغو گردید.'})