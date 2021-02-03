from django.contrib import admin
from django.utils.html import format_html

from .models import Order


# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_filter = ('status', 'fcuser')  # tuple
    list_display = ('fcuser', 'product', 'quantity', 'styled_status')

    def styled_status(self, obj):
        return format_html('<b>test</b>')  # obj.status


admin.site.register(Order, OrderAdmin)
