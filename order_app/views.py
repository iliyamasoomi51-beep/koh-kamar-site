from django.http import HttpRequest, JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from .models import Order, OrderDetail, Product
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required



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