from django.contrib import admin
from .models import Fcuser


# Register your models here.


class FcuserAdmin(admin.ModelAdmin):
    list_display = ('email', 'password')


admin.site.register(Fcuser, FcuserAdmin)

# admin theme
admin.site.site_header = 'fastcampus jjaen'
admin.site.index_title = 'fastcampus admin'
admin.site.site_title = 'fastcampus jjaen'
