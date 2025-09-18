
from django.http import HttpRequest, JsonResponse
from product_app.models import Product
from .models import Order, OrderDetail


# def add_product_to_order(request: HttpRequest):
#     if request.method != 'POST':
#         return JsonResponse({'status': 'invalid_method', 'text': 'متد درخواست نامعتبر است'})
#
#     try:
#         product_id = int(request.POST.get('product_id'))
#         count = int(request.POST.get('count'))
#     except (ValueError, TypeError):
#         return JsonResponse({
#             'status': 'invalid_input',
#             'text': 'اطلاعات ارسالی نامعتبر است',
#             'confirm_button_text': 'چشم',
#             'icon': 'error'
#         })
#
#     if count < 1:
#         return JsonResponse({
#             'status': 'invalid_count',
#             'text': 'مقدار وارد شده معتبر نیست',
#             'confirm_button_text': 'چشم',
#             'icon': 'warning'
#         })
#
#     if not request.user.is_authenticated:
#         return JsonResponse({
#             'status': 'not_logged_in',
#             'text': 'برای افزودن به سبدخرید ابتدا باید وارد سایت شوید',
#             'confirm_button_text': 'ورود به سایت',
#             'icon': 'error'
#         })
#
#     product = Product.objects.filter(id=product_id, available=True).first()
#     if product is None:
#         return JsonResponse({
#             'status': 'not_found',
#             'text': 'محصول مورد نظر یافت نشد',
#             'confirm_button_text': 'چشم چک میکنم',
#             'icon': 'error'
#         })
#
#     current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
#     order_detail, detail_created = current_order.orderdetails_set.get_or_create(
#         product_id=product_id,
#         defaults={'count': count}
#     )
#
#     if not detail_created:
#         order_detail.count += count
#         order_detail.save()
#
#     return JsonResponse({
#         'status': 'success',
#         'text': 'محصول مورد نظر با موفقیت به سبد خرید شما اضافه شد',
#         'confirm_button_text': 'باشه ممنونم',
#         'icon': 'success'
#     })

def add_product_to_order(request: HttpRequest):
    print("1. Function started.")

    if request.method != 'POST':
        print("2. Method is not POST.")
        return JsonResponse({'status': 'invalid_method', 'text': 'متد درخواست نامعتبر است'})

    try:
        product_id = int(request.POST.get('product_id'))
        count = int(request.POST.get('count'))
        print(f"3. Received data: product_id={product_id}, count={count}")
    except (ValueError, TypeError):
        print("4. Invalid input received.")
        return JsonResponse({
            'status': 'invalid_input',
            'text': 'اطلاعات ارسالی نامعتبر است',
            'confirm_button_text': 'چشم',
            'icon': 'error'
        })

    if count < 1:
        print("5. Invalid count (less than 1).")
        return JsonResponse({
            'status': 'invalid_count',
            'text': 'مقدار وارد شده معتبر نیست',
            'confirm_button_text': 'چشم',
            'icon': 'warning'
        })

    if not request.user.is_authenticated:
        print("6. User is not authenticated.")
        return JsonResponse({
            'status': 'not_logged_in',
            'text': 'برای افزودن به سبدخرید ابتدا باید وارد سایت شوید',
            'confirm_button_text': 'ورود به سایت',
            'icon': 'error'
        })

    product = Product.objects.filter(id=product_id, available=True).first()
    if product is None:
        print("7. Product not found or not available.")
        return JsonResponse({
            'status': 'not_found',
            'text': 'محصول مورد نظر یافت نشد',
            'confirm_button_text': 'چشم چک میکنم',
            'icon': 'error'
        })

    print("8. Product found. Moving to order logic.")
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    order_detail, detail_created = current_order.orderdetails_set.get_or_create(
        product_id=product_id,
        defaults={'count': count}
    )

    if not detail_created:
        print("9. Updating existing order detail.")
        order_detail.count += count
        order_detail.save()
    else:
        print("10. Creating new order detail.")

    print("11. Operation successful.")
    return JsonResponse({
        'status': 'success',
        'text': 'محصول مورد نظر با موفقیت به سبد خرید شما اضافه شد',
        'confirm_button_text': 'باشه ممنونم',
        'icon': 'success'
    })

    # اگر به هر دلیلی هیچ کدام از return ها اجرا نشدند، یک پاسخ پیش‌فرض ارسال می‌کنیم
    print("12. No return statement was reached. Something went wrong.")
    return JsonResponse({'status': 'unknown_error', 'text': 'خطای نامشخص رخ داده است.'})