import re
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views import generic, View

from .models import *
from .forms import *

# Create your views here.
class BasketCartView(LoginRequiredMixin, View):
    """
    View for Show Detail of Basket Cart for Customer
    """

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(id=request.user.id)
        order = customer.orders.filter(status__exact='U')
        order = order[0] if order.count() == 1 else None
        form = OrderForm(instance=order)
        return render(request, "order/cart.html", {
            'order': order, 'form': form,
        })

    def post(self, request, *args, **kwargs):
        customer = Customer.objects.get(id=request.user.id)
        order = customer.orders.filter(status='U')[0]
        form = OrderForm(request.POST)
        if form.is_valid():
            order.code = request.POST["code"] or None
            order.save()
            return redirect(reverse("order:cart"))
        order.code = None
        order.save()
        return render(request, "order/cart.html", {
            'order': order, 'form': form,
        })


class ChangeCountItemView(LoginRequiredMixin, View):
    """
    View for Return Form Order Item Check Validated Change Count
    """

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(id=request.user.id)
        item = OrderItem.objects.get(id=self.request.GET['item'])
        if item.order.status == 'U' and item.order.customer == customer:
            form = OrderItemForm(instance=item)
            return render(request, "order/items.html", {
                'product': item.product, 'form': form,
            })
        return redirect(reverse("order:cart"))
    
    def post(self, request, *args, **kwargs):
        customer = Customer.objects.get(id=request.user.id)
        item = OrderItem.objects.get(id=self.request.GET['item'])
        form = OrderItemForm(request.POST)
        if form.is_valid():
            item.count = request.POST["count"]
            item.save()
            return redirect(reverse("order:cart"))
        return render(request, "order/items.html", {
            'product': item.product, 'form': form,
        })


class OrdersCustomerView(LoginRequiredMixin, generic.ListView):
    """
    Show History of Orders List for Customer Can Filter by Status
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


class ChangeCartStatusView(LoginRequiredMixin, View):
    """
    View for Change Status of Order to Paid or Canceling
    """

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(id=request.user.id)
        order = customer.orders.get(id=self.request.GET['order'])
        if order.customer == customer:
            if self.request.GET['status'] == 'P':
                order.payment()
                order.save()
            if self.request.GET['status'] == 'C':
                order.cancel()
                order.save()
        return redirect(reverse("order:orders"))
