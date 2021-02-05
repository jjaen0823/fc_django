from django.contrib import admin
from .models import Fcuser


# Register your models here.


class FcuserAdmin(admin.ModelAdmin):
    list_display = ('email', 'password')

    def changelist_view(self, request, extra_context=None):
        #
        extra_context = {'title': 'User List'}
        return super().changelist_view(request, extra_context)

    # def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
    #     fcuser = Fcuser.objects.get(pk=object_id)  # 예외처리 따로 하지 않음
    #     extra_context = {'title': f'{fcuser.email} Update'}
    #     return super().changeform_view(request, object_id, form_url, extra_context)


admin.site.register(Fcuser, FcuserAdmin)

# admin theme
admin.site.site_header = 'fastcampus jjaen'
admin.site.index_title = 'fastcampus admin'
admin.site.site_title = 'fastcampus jjaen'
