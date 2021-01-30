from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.views.generic.edit import FormView

from .forms import RegisterForm, LoginForm
from .models import Fcuser


# Create your views here.


def index(request):
    email = request.session.get('user')
    return render(request, 'fcuser/index.html', {'email': email})


class RegisterView(FormView):
    template_name = 'fcuser/register.html'  # html file
    form_class = RegisterForm  # form 등록
    success_url = '/'

    def form_valid(self, form):  # 유효성 검사가 끝났을 때 호출되는 함수
        # register code
        fcuser = Fcuser(
            email=form.data.get('email'),
            password=make_password(form.data.get('password')),
            level='user',
        )
        fcuser.save()

        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'fcuser/login.html'  # html file
    form_class = LoginForm  # form 등록
    success_url = '/'

    # session
    def form_valid(self, form):
        self.request.session['user'] = form.data.get('email')

        return super().form_valid(form)


def logout(request):
    if request.session.get('user'):  # if 'user' in request.session":
        del(request.session['user'])
    return redirect('/')
