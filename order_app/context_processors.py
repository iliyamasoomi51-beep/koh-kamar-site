from .models import Order
from django.db.models import F

def cart_context(request):
    cart_items = []
    total_price = 0
    if request.user.is_authenticated:
        try:
            cart, created = Order.objects.get_or_create(user=request.user, is_paid=False)
            cart_items = cart.orderdetails_set.all()
            total_price = cart.calculate_total_price()
        except Exception:
            pass

    return {
        'cart': cart_items,
        'total_price': total_price
    }