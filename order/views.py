from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import FormView

from django.utils.decorators import method_decorator
from fcuser.decorators import login_required

from django.db import transaction

from .forms import RegisterForm
from .models import Order
from fcuser.models import Fcuser
from product.models import Product

# Create your views here.


@method_decorator(login_required, name='dispatch')
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

    # url에 접근해서 ClassView를 호출할 때 불리는 함수가 dispatch이다
    # @login_required
    # def dispatch(self, request, *args, **kwargs): -> method_decoration 사용하면 class에 바로 적용 가능


@method_decorator(login_required, name='dispatch')
class OrderCreate(FormView):
    form_class = RegisterForm
    success_url = '/product/'

    def form_valid(self, form):
        quantity = form.data.get('quantity')
        product = form.data.get('product')
        fcuser = Fcuser.objects.get(email=self.request.session.get(
            'user'))  # 해당 fcuser 객체에 대한 pk 를 가지고 옴

        if int(quantity) < 0:
            return redirect('/product/' + str(product))

        with transaction.atomic():
            prod = Product.objects.get(pk=product)
            if prod.stock is None:
                return redirect('/product/' + str(product))

            order = Order(
                quantity=quantity,
                product=prod,
                fcuser=fcuser,
            )
            order.save()
            prod.stock -= int(quantity)
            prod.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        product = form.data.get('product')
        return redirect('/product/' + str(product))

    # FormView 안에서도 request를 전달할 수 있도록 만들어줘야 함

    def get_form_kwargs(self, **kwargs):
        # form을 생성할 때 어떤 인자값을 전달해서 만들 것인지 결정하는 함수
        kw = super().get_form_kwargs(**kwargs)
        kw.update({
            'request': self.request
        })
        return kw
