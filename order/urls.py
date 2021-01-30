from django.contrib import admin
from django.urls import path

from order.views import OrderCreate, OrderList


urlpatterns = [
    path('', OrderList.as_view(), name='order'),
    path('create/', OrderCreate.as_view(), name='create'),
]
