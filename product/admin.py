from django.db.models import Q
from django.db import transaction
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType

from django.contrib import admin
from django.utils.html import format_html

from django.contrib.humanize.templatetags.humanize import intcomma

from django.urls import path
from django.template.response import TemplateResponse
import datetime

from .models import Product


# Register your models here.

# def delete(modelAdmin, request, queryset):
#     with transaction.atomic():
#         qs = queryset.filter(~Q())


class ProductAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    list_display = ('name', 'price_format', 'styled_stock', 'action')
    change_list_template = 'admin/product_change_list.html'

    def action(self, obj):
        return format_html(f'<input type="button" value="delete" onclick="product_change_submit({obj.id})" class="btn btn-primary btn-sm">')

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
        extra_context = {'title': 'Product List'}
        #
        if request.method == 'POST':
            # button을 만들 때 id를 담아서 post해줘야 함
            # print(request.POST)
            obj_id = request.POST.get('obj_id')
            if obj_id:
                qs = Product.objects.filter(pk=obj_id)
                ct = ContentType.objects.get_for_model(qs.model)
                for obj in qs:
                    obj.delete()

        return super().changelist_view(request, extra_context)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        product = Product.objects.get(pk=object_id)  # 예외처리 따로 하지 않음
        extra_context = {
            'title': f'{product.name} Update'
        }
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super().changeform_view(request, object_id, form_url, extra_context)

    def get_urls(self):
        urls = super().get_urls()
        date_urls = [
            path('date_view/', self.date_view),
        ]
        return date_urls + urls

    def date_view(self, request):
        week_date = datetime.datetime.now() - datetime.timedelta(days=7)
        week_data = Product.objects.filter(register_date__gte=week_date)
        data = Product.objects.filter(register_date__lt=week_date)

        context = dict(
            self.admin_site.each_context(request),
            week_data=week_data,
            data=data,
        )

        return TemplateResponse(request, 'admin/product_date_view.html', context)


admin.site.register(Product, ProductAdmin)
