from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views import generic, View

from .models import *
from .forms import *

# Create your views here.
class BasketCartView(LoginRequiredMixin, View):
    """
    
    """

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(id=request.user.id)
        order = customer.orders.filter(status__exact='U')[0]
        form = OrderForm(instance=order)
        return render(request, "order/cart.html", {
            'order': order, 'form': form
        })

    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST)
        if form.is_valid():
            print("YESSS")
        return HttpResponse("OK!")


class OrdersCustomerView(LoginRequiredMixin, generic.ListView):
    """
    
    """

    context_object_name = "orders"
    template_name = "order/orders.html"

    def get_queryset(self):
        customer = Customer.objects.get(id=self.request.user.id)
        result = customer.orders.exclude(status__exact='U')
        kwargs = self.request.GET
        if "status" in kwargs:
            result = result.filter(status__exact=kwargs["status"])
        return result
