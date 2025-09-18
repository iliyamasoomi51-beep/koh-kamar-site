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

    def calculate_total_price(self):
        """
        قیمت کل سبد خرید را با استفاده از Aggregation دیتابیس محاسبه می‌کند.
        """
        # از annotate برای اضافه کردن فیلد موقت 'item_price' (قیمت * تعداد) استفاده می‌کنیم
        annotated_details = self.orderdetails_set.annotate(
            item_price=F('final_price') * F('count')
        )
        # با استفاده از Sum، قیمت کل را به دست می‌آوریم
        total = annotated_details.aggregate(total_price=Sum('item_price'))['total_price']

        # اگر سبد خرید خالی بود، 0 را برمی‌گرداند
        return total if total is not None else 0

    def decrease_product_stock(self):
        """
        موجودی هر محصول در سبد خرید را بعد از نهایی شدن سفارش، کاهش می‌دهد.
        """
        if self.is_paid:
            for detail in self.orderdetails_set.all():
                # موجودی فعلی را با استفاده از F() به صورت اتمیک کم می‌کند
                # این کار از بروز مشکلات در صورت پردازش همزمان چندین سفارش جلوگیری می‌کند
                Product.objects.filter(id=detail.product.id).update(
                    stock=F('stock') - detail.count
                )
        else:
            # اگر سبد خرید نهایی نشده بود، پیامی نمایش می‌دهد
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