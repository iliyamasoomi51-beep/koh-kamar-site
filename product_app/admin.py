from django.contrib import admin

from .models import Product , Category , ProductImage


from django.contrib import admin
from .models import Category, Product, ProductImage  # مدل جدید را import کنید

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug',]
    prepopulated_fields = {'slug': ('name',)}


# یک کلاس inline برای تصاویر گالری بسازید
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # تعداد فرم‌های خالی برای آپلود عکس جدید


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created','stock']
    list_filter = ['available', 'created']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    # inline را به ادمین محصول اضافه کنید
    inlines = [ProductImageInline]
