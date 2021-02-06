from django.db.models import Q
from django.db import transaction
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType

from django.contrib import admin
from django.utils.html import format_html

from .models import Fcuser


# Register your models here.


class FcuserAdmin(admin.ModelAdmin):
    list_display = ('email', 'password', 'action')
    change_list_template = 'admin/fcuser_delete_list.html'

    def action(self, obj):
        return format_html(f'<input type="button" value="delete" onclick="fcuser_delete_submit({obj.id})" class="btn btn-primary btn-sm">')

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'User List'}
        #
        if request.method == 'POST':
            print(request.POST)
            obj_id = request.POST.get('obj_id')
            if obj_id:
                qs = Fcuser.objects.filter(pk=obj_id)
                ct = ContentType.objects.get_for_model(qs.model)
                for obj in qs:
                    obj.delete()

        return super().changelist_view(request, extra_context)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        fcuser = Fcuser.objects.get(pk=object_id)  # 예외처리 따로 하지 않음
        extra_context = {
            'title': f'{fcuser.email} Update'
        }
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super().changeform_view(request, object_id, form_url, extra_context)


admin.site.register(Fcuser, FcuserAdmin)

# admin theme
admin.site.site_header = 'fastcampus jjaen'
admin.site.index_title = 'fastcampus admin'
admin.site.site_title = 'fastcampus jjaen'
