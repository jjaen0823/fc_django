from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import FormView

from .forms import RegisterForm
from .models import Order

# Create your views here.


class OrderList(ListView):
    template_name = 'order/order.html'
    # variable name to use in template(html)
    context_object_name = 'order_list'

    # model = Order  # 모든 order 전달받음 -> Use quaryset
    # session 도 필요해서 queryset 그대로 쓸 수 없음
    # Overriding
    def get_queryset(self, **kwargs):
        queryset = Order.objects.filter(
            fcuser__email=self.request.session.get('user'))
        return queryset


class OrderCreate(FormView):
    form_class = RegisterForm
    success_url = '/product/'

    def form_invalid(self, form):
        return redirect('/product/' + str(form.product))

    # FormView 안에서도 request를 전달할 수 있도록 만들어줘야 함

    def get_form_kwargs(self, **kwargs):
        # form을 생성할 때 어떤 인자값을 전달해서 만들 것인지 결정하는 함수
        kw = super().get_form_kwargs(**kwargs)
        kw.update({
            'request': self.request
        })
        return kw
