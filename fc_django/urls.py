"""fc_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.template.response import TemplateResponse

from django.views.generic import TemplateView

import datetime

from fcuser.views import *
# import fcuser.urls
import product.urls
from product.views import (
    ProductListAPI, ProductDetailAPI
)
import order.urls
from order.models import Order

from .functions import get_exchange


orig_index = admin.site.index


def fc_index(request, extra_context=None):
    base_date = datetime.datetime.now() - datetime.timedelta(days=7)
    order_data = {}
    for idx in range(7):
        target_dttm = base_date + datetime.timedelta(days=idx)
        date_key = target_dttm.strftime('%Y-%m-%d')
        target_date = datetime.date(
            target_dttm.year, target_dttm.month, target_dttm.day)
        order_cnt = Order.objects.filter(
            register_date__date=target_date).count()
        order_data[date_key] = order_cnt

    extra_context = {
        'orders': order_data,
        'exchange': get_exchange()
    }

    # return TemplateResponse(request, 'admin/index.html', extra_context)
    return orig_index(request, extra_context)


admin.site.index = fc_index


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^admin/manual/$',
            TemplateView.as_view(
                template_name='admin/manual.html',
                extra_context={'title': 'Manual', 'site_title': 'fastcampus jjaen',
                               'site_header': 'Fastcampus jjaen'},
            )
            ),

    path('baton/', include('baton.urls')),

    path('', index, name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path('product/', include(product.urls)),
    path('order/', include(order.urls)),

    path('api/product/', ProductListAPI.as_view()),
    path('api/product/<int:pk>/', ProductDetailAPI.as_view()),
]
