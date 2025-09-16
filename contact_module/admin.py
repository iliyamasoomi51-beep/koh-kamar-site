from django.contrib import admin

from contact_module import models


class Contact_admin(admin.ModelAdmin):
    list_display = ['contact_title' , 'contact_fullname' , 'contact_is_read_admin']
    list_editable = ['contact_is_read_admin']



admin.site.register(models.Contact, Contact_admin)


