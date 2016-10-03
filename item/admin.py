from django.contrib import admin

# Register your models here.
from .models import Item

# class ItemAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('name',)}
#
# admin.site.register(Item, ItemAdmin)
admin.site.register(Item)
