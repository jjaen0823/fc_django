from django.contrib import admin
from django.urls import path

from product.views import ProductList, ProductCreate


urlpatterns = [
    path('', ProductList.as_view(), name='product'),
    path('create/', ProductCreate.as_view(), name='create'),
]
