from django.contrib import admin

from .models import Order


# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'userprofile', 'receiver')


admin.site.register(Order, OrderAdmin)
