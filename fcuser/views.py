from django.shortcuts import render
from django.views.generic.edit import FormView

from .forms import RegisterForm, LoginForm


# Create your views here.
def index(request):
    email = request.session.get('user')
    return render(request, 'fcuser/index.html', {'email': email})


class RegisterView(FormView):
    template_name = 'fcuser/register.html'  # html file
    form_class = RegisterForm  # form 등록
    success_url = '/'


class LoginView(FormView):
    template_name = 'fcuser/login.html'  # html file
    form_class = LoginForm  # form 등록
    success_url = '/'

    # session
    def form_valid(self, form):
        self.request.session['user'] = form.email

        return super().form_valid(form)
