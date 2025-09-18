
from django.http import HttpRequest, JsonResponse
from product_app.models import Product
from .models import Order, OrderDetail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy



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


    if request.method != 'POST':

        return JsonResponse({'status': 'invalid_method', 'text': 'متد درخواست نامعتبر است'})

    try:
        product_id = int(request.POST.get('product_id'))
        count = int(request.POST.get('count'))
        print(f"3. Received data: product_id={product_id}, count={count}")
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

    if not request.user.is_authenticated:

        return JsonResponse({
            'status': 'not_logged_in',
            'text': 'برای افزودن به سبدخرید ابتدا باید وارد سایت شوید',
            'confirm_button_text': 'ورود به سایت',
            'confirm_button_url': reverse_lazy('login_or_register_page'),  # تولید URL برای لاگین
            'icon': 'error'
        })


    product = Product.objects.filter(id=product_id, available=True).first()
    if product is None:

        return JsonResponse({
            'status': 'not_found',
            'text': 'محصول مورد نظر یافت نشد',
            'confirm_button_text': 'چشم چک میکنم',
            'icon': 'error'
        })


    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    order_detail, detail_created = current_order.orderdetails_set.get_or_create(
        product_id=product_id,
        defaults={'count': count}
    )

    if not detail_created:

        order_detail.count += count
        order_detail.save()


    return JsonResponse({
        'status': 'success',
        'text': 'محصول مورد نظر با موفقیت به سبد خرید شما اضافه شد',
        'confirm_button_text': 'باشه ممنونم',
        'icon': 'success'
    })



def cart_detail(request):
    # سبد خرید رو از سشن می‌گیره، اگه وجود نداشت، یک دیکشنری خالی ایجاد می‌کنه
    cart = request.session.get('cart', {})
    cart_items_list = []
    total_price = 0

    # از اطلاعات داخل سشن استفاده می‌کنه تا آبجکت‌های محصول رو از دیتابیس بگیره
    for product_id, item_data in cart.items():
        try:
            # مطمئن میشه که محصول با این ID در دیتابیس وجود داره
            product = Product.objects.get(id=product_id)
            item_total = product.price * item_data['quantity']
            cart_items_list.append({
                'product': product,
                'quantity': item_data['quantity'],
                'total_item_price': item_total
            })
            total_price += item_total
        except Product.DoesNotExist:

            del cart[product_id]

    request.session['cart'] = cart

    context = {
        'cart': cart_items_list,
        'total_price': total_price
    }
    return render(request, 'cart/new_cart.html', context)


# تابع برای اضافه کردن محصول به سبد خرید
def add_to_cart(request, product_id):
    # محصول رو بر اساس ID پیدا می‌کنه یا خطای 404 برمی‌گردونه
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    # اگه محصول از قبل در سبد هست، فقط تعدادش رو زیاد می‌کنه
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        # اگه محصول جدید هست، اون رو به سبد اضافه می‌کنه
        cart[str(product_id)] = {'quantity': 1}

    request.session['cart'] = cart
    return redirect('cart_detail')


# تابع برای حذف یک محصول از سبد خرید
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    # اگه محصول در سبد خرید وجود داره، اون رو حذف می‌کنه
    if str(product_id) in cart:
        del cart[str(product_id)]

    request.session['cart'] = cart
    return redirect('cart_detail')