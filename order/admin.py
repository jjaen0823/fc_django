from django.contrib import admin
from django.utils.html import format_html

from .models import Order


# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_filter = ('status', 'fcuser')  # tuple
    # using function_name in list_display
    list_display = ('fcuser', 'product', 'quantity', 'styled_status')

    def styled_status(self, obj):
        # '<b>' + obj.status + '</b>'
        # '<b>%s</b>' % (obj.status)
        # '<b>{}</b>'.format(obj.status)
        # f'<b><{obj.status}/b>'
        status = obj.status
        if status == 'waiting':
            return format_html('<span style="color:blue">{}</span>'.format(status))
        elif status == 'payment':
            return format_html('<span style="color:green">{}</span>'.format(status))
        elif status == 'refund':
            return format_html('<span style="color:red">{}</span>'.format(status))
        return format_html('<b>{}</b>'.format(status))  # obj.status

    styled_status.short_description = 'status'  # change function description


admin.site.register(Order, OrderAdmin)
