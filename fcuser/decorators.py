from django.shortcuts import redirect

from .models import Fcuser


def login_required(function):
    def wrap(request, *args, **kwargs):  # wrapping 한 함수와 기존 함수의 parameter를 맞춰줘야 함
        user = request.session.get('user')
        if user is None or not user:  # user가 없거나 비어있거나
            return redirect('/login')
        return function(request, *args, **kwargs)

    return wrap


# @login_required
def admin_required(function):
    def wrap(request, *args, **kwargs):  # wrapping 한 함수와 기존 함수의 parameter를 맞춰줘야 함
        user = request.session.get('user')
        if user is None or not user:  # user가 없거나 비어있거나
            return redirect('/login')

        user = Fcuser.objects.get(email=user)
        if user.level != 'admin':
            return redirect('/')

        return function(request, *args, **kwargs)

    return wrap
