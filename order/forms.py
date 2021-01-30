from django import forms
from django.db import transaction

from .models import Order
from product.models import Product
from fcuser.models import Fcuser


class RegisterForm(forms.Form):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    quantity = forms.IntegerField(
        error_messages={
            'required': 'Please enter the quantity of the product.'
        },
        label='Quantity'
    )

    # login 된 시용자 정보가 자동으로 전달되기 때문에 form에서 다루지 않아도 됨

    product = forms.IntegerField(
        error_messages={
            'required': 'Please enter the description of your product.'
        },
        label='Product',
        widget=forms.HiddenInput
    )

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        product = cleaned_data.get('product')  # 해당 product 객체에 대한 pk 를 가지고 옴
        fcuser = self.request.session.get(
            'user')  # 해당 fcuser 객체에 대한 pk 를 가지고 옴

        if quantity and quantity > 0 and product and fcuser:
            with transaction.atomic():
                prod = Product.objects.get(pk=product)
                order = Order(
                    quantity=quantity,
                    product=prod,
                    fcuser=Fcuser.objects.get(email=fcuser)
                )
                order.save()
                prod.stock -= quantity
                prod.save()
        else:
            self.product = product
            self.add_error('quantity', 'There is no quantity.')
            self.add_error('product', 'There is no product.')
