from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    avatar = models.ImageField(max_length=120 , verbose_name= 'تصویر اواتار',null=True, blank=True)
    verification_code = models.CharField(max_length=5 , blank=True,null=True)
    mobile = models.CharField(max_length=200 , verbose_name='شماره تلفن')
    groups = models.ManyToManyField(

        'auth.Group',
        related_name='account_users',
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='account_users_permissions',
        blank=True,
    )
    class Meta:
        verbose_name="کاربر"
        verbose_name_plural="کاربران"




    def __str__(self):
     if self.first_name is not '' and self.last_name is not '':
         return self.get_full_name()
     return self.email