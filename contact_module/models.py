
from django.db import models


class Contact(models.Model):
    contact_title = models.CharField(max_length=100, verbose_name='عنوان پیام')
    contact_email = models.EmailField(verbose_name='ایمیل')
    contact_fullname = models.CharField(max_length=50, verbose_name='نام و نام خانوادگی')
    contact_phone_number = models.CharField(max_length=12, verbose_name='شماره تماس')
    contact_message = models.TextField(verbose_name='متن پیام مخاطب')
    contact_admin_message = models.TextField(verbose_name='پیام ادمین')
    contact_is_read_admin = models.BooleanField(default=False, verbose_name='خوانده شده / خوانده نشده')
    contact_created_data = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت پیام')

    def __str__(self):
        return self.contact_title


