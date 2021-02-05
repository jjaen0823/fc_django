from django.db.models import Q  # F: 기존의 db에 들어있는 값에다가 변경할 때 사용한다.
from django.db import transaction
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType

from django.contrib import admin
from django.utils.html import format_html

from .models import Order

# Register your models here.


def refund(modelAdmin, request, queryset):  # queryset에는 admin에서 체크한 객체들이 들어옴
    with transaction.atomic():
        qs = queryset.filter(~Q(status='refund'))  # queryset 응용
        # model type을 알려줘야 함
        ct = ContentType.objects.get_for_model(queryset.model)
        for obj in qs:
            obj.product.stock += obj.quantity
            obj.product.save()

            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ct.pk,
                object_id=obj.pk,
                object_repr=f'{obj.fcuser.email} refund',
                action_flag=CHANGE,
                change_message='refund',
            )
            print(obj.fcuser.email)

        qs.update(status='refund')

    """
    for obj in queryset:
        if obj.status == 'refund':
            continue
        else:  # obj.status != 'refund'
            obj.product.stock += obj.quantity
            obj.product.save()

    queryset.update(status='refund')
    """


refund.short_description = 'Refund'


class OrderAdmin(admin.ModelAdmin):
    """
    ModelAdmin 옵션
        list_display : Admin 목록에 보여질 필드 목록
        list_display_links : 목록 내에서 링크로 지정할 필드 목록 (이를 지정하지 않으면, 첫번째 필드에만 링크가 적용)
        list_editable : 목록 상에서 수정할 필드 목록
        list_per_page : 페이지 별로 보여질 최대 갯수 (디폴트 : 100)
        list_filter : 필터 옵션을 제공할 필드 목록
        actions : 목록에서 수행할 action 목록
    """
    list_filter = ('status', )  # tuple
    # using function_name in list_display
    list_display = ('fcuser', 'product', 'quantity', 'styled_status', 'action')
    change_list_template = 'admin/order_change_list.html'

    # actions에 등록되어 있는 함수에 필요한 parameter를 전달해줌
    actions = [
        refund
    ]

    def action(self, obj):
        if obj.status != 'refund':
            return format_html(f'<input type="button" value="refund" onclick="order_refund_submit({obj.id})" class="btn btn-primary btn-sm">')
        else:
            return

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

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Order List'}
        #
        if request.method == 'POST':
            # button을 만들 때 id를 담아서 post해줘야 함
            # print(request.POST)
            obj_id = request.POST.get('obj_id')
            if obj_id:
                qs = Order.objects.filter(pk=obj_id)
                ct = ContentType.objects.get_for_model(qs.model)
                for obj in qs:
                    obj.product.stock += obj.quantity
                    obj.product.save()

                    LogEntry.objects.log_action(
                        user_id=request.user.id,
                        content_type_id=ct.pk,
                        object_id=obj.pk,
                        object_repr=f'{obj.fcuser.email} refund',
                        action_flag=CHANGE,
                        change_message='refund',
                    )
                qs.update(status='refund')

        return super().changelist_view(request, extra_context)

    # def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
    #     order = Order.objects.get(pk=object_id)  # 예외처리 따로 하지 않음
    #     extra_context = {
    #         'title': f"'{order.fcuser.email}'의 '{order.product.name}' Order Update"
    #     }
    #     return super().changeform_view(request, object_id, form_url, extra_context)


admin.site.register(Order, OrderAdmin)
