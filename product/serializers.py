from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'  # field를 지정하지 않으면 자동으로 model 안의 모든 field를 가져옴
