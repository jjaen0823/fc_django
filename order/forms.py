from django import forms
from .models import Order


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
        product = cleaned_data.get('product')
