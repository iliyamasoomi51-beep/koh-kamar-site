from django.db import models
from django.db.models import F, Sum
from account_moduels.models import User
from product_app.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    is_paid = models.BooleanField(verbose_name="نهایی شده/نشده")
    payment_date = models.DateField(verbose_name='تاریخ پرداخت', null=True, blank=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد های خرید کاربران'

    # در فایل models.py
    # در کلاس Order
    def calculate_total_price(self):
        total = 0
        # به جای Aggregate، روی OrderDetailها حلقه می‌زنیم
        for item in self.orderdetails_set.all():
            # اگر final_price مقدار نداشت، از صفر استفاده کن
            final_price = item.final_price if item.final_price is not None else 0
            total += final_price * item.count
        return total

    def decrease_product_stock(self):
        """
        موجودی هر محصول در سبد خرید را بعد از نهایی شدن سفارش، کاهش می‌دهد.
        """
        if self.is_paid:
            for detail in self.orderdetails_set.all():

                Product.objects.filter(id=detail.product.id).update(
                    stock=F('stock') - detail.count
                )
        else:

            print("Error: Cannot decrease stock for an unpaid order.")


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سبد خرید', related_name='orderdetails_set')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    final_price = models.IntegerField(null=True, blank=True, verbose_name='قیمت نهایی تک محصول')
    count = models.IntegerField(verbose_name='تعداد')

    def __str__(self):
        return str(self.order)

    class Meta:
        verbose_name = 'جزئیات سبد خرید'
        verbose_name_plural = 'لیست جزئیات سبد خرید'




# این مدل‌ها را به فایل models.py خود اضافه کنید

class FinalOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    # این فیلد به سبد خرید موقت (Order) که نهایی شده است، اشاره می‌کند
    original_cart = models.OneToOneField(Order, on_delete=models.PROTECT, verbose_name='سبد خرید اصلی')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='مبلغ نهایی')
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ پرداخت')

    def __str__(self):
        return f"Final Order {self.id}"

    class Meta:
        verbose_name = 'سفارش نهایی'
        verbose_name_plural = 'سفارشات نهایی'

class FinalOrderDetail(models.Model):
    final_order = models.ForeignKey(FinalOrder, on_delete=models.CASCADE, verbose_name='سفارش نهایی', related_name='final_order_details')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='محصول')
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='قیمت در زمان خرید')
    count = models.IntegerField(verbose_name='تعداد')

    def __str__(self):
        return str(self.product.name)

    class Meta:
        verbose_name = 'جزئیات سفارش نهایی'
        verbose_name_plural = 'جزئیات سفارشات نهایی'