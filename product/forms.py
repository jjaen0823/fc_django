from django import forms
from .models import Product


class RegisterForm(forms.Form):
    name = forms.CharField(
        error_messages={
            'required': 'Please enter your product name.'
        },
        max_length=64,
        label='Product Name'
    )

    price = forms.IntegerField(
        error_messages={
            'required': 'Please enter the price of your product.'
        },
        label='Price'
    )

    description = forms.CharField(
        error_messages={
            'required': 'Please enter the description of your product.'
        },
        label='Description'
    )

    stock = forms.IntegerField(
        error_messages={
            'required': 'Please enter the stock of your product.'
        },
        label='Stock'
    )

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        price = cleaned_data.get('price')
        description = cleaned_data.get('description')
        stock = cleaned_data.get('stock')

        """
        if name and price and description and stock:
            # register code
            product = Product(
                name=name,
                price=price,
                description=description,
                stock=stock,
            )
            product.save()
        """
        if not (name and price and description and stock):  # You can pass error message seperately for each variable.
            self.add_error('name', 'There is no product name.')
            self.add_error('price', 'There is no price.')
            self.add_error('description', 'There is no description.')
            self.add_error('stock', 'There is no stock.')
