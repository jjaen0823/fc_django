from django import forms
from django.contrib.auth.hashers import make_password, check_password
from .models import Fcuser


class RegisterForm(forms.Form):
    email = forms.EmailField(
        error_messages={
            'required': 'Please enter your email.'
        },
        max_length=64,
        label='Email'
    )

    password = forms.CharField(
        error_messages={
            'required': 'Please enter your password.'
        },
        widget=forms.PasswordInput,
        label='Password'
    )

    re_password = forms.CharField(
        error_messages={
            'required': 'Please enter your password again.'
        },
        widget=forms.PasswordInput,
        label='re_Password'
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')

        if password and re_password:
            if password != re_password:
                # Add error message to re_password field.
                self.add_error('re_password', 'Password is different!')
            else:
                # register code
                fcuser = Fcuser(
                    email=email,
                    password=make_password(password)
                )
                fcuser.save()


class LoginForm(forms.Form):
    email = forms.EmailField(
        error_messages={
            'required': 'Please enter your email.'
        },
        max_length=64,
        label='Email'
    )

    password = forms.CharField(
        error_messages={
            'required': 'Please enter your password.'
        },
        widget=forms.PasswordInput,
        label='Password'
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                fcuser = Fcuser.objects.get(email=email)
            except Fcuser.DoesNotExist:
                self.add_error('email', 'User does not exist.')
                return

            if not check_password(password, fcuser.password):
                self.add_error('password', 'Your Password is wrong!')
            else:
                self.email = fcuser.email
