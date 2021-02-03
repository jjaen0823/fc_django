from django.contrib import admin
from django.utils.html import format_html
from django.contrib.humanize.templatetags.humanize import intcomma

from .models import Product


# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    list_display = ('name', 'price_format', 'styled_stock')

    def styled_stock(self, obj):
        stock = intcomma(obj.stock)  # str
        if obj.stock <= 50:
            return format_html('<b><span style="color:red">{} 개</span></b>'.format(stock))
        return '{} 개'.format(stock)  # obj.status

    def price_format(self, obj):
        price = intcomma(obj.price)  # str
        return '{} won'.format(price)

    styled_stock.short_description = 'stock'
    price_format.short_description = 'price'


admin.site.register(Product, ProductAdmin)
