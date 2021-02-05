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

    def changelist_view(self, request, extra_context=None):
        #
        extra_context = {'title': 'Product List'}
        return super().changelist_view(request, extra_context)

    # def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
    #     product = Product.objects.get(pk=object_id)  # 예외처리 따로 하지 않음
    #     extra_context = {'title': f'{product.name} Update'}
    #     return super().changeform_view(request, object_id, form_url, extra_context)


admin.site.register(Product, ProductAdmin)
