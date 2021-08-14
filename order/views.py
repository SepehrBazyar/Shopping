from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views import generic, View
from django.utils.translation import gettext_lazy as _
from django.contrib import messages

from .models import *
from .forms import *

# Create your views here.
class BasketCartView(LoginRequiredMixin, View):
    """
    View for Show Detail of Basket Cart for Customer
    """

    def get(self, request, *args, **kwargs):
        msgs = messages.get_messages(request)
        try: customer = Customer.objects.get(id=request.user.id)
        except Customer.DoesNotExist: return redirect(reverse("customer:logout"))
        if customer.addresses.count() == 0:
            return redirect(reverse("customer:address"))
        new_items = set(request.COOKIES.get("cart", "").split(',')[:-1])
        order = customer.orders.filter(status__exact='U')
        if order.count() == 1:
            order = order[0]
            for item in new_items:
                product = Product.objects.get(id=int(item))
                if order.items.filter(product=product).count() == 0:
                    OrderItem.objects.create(order=order, product=product, count=1)
        else:
            if new_items:
                order = Order.objects.create(
                    customer=customer, address=customer.addresses.first())
                for item in new_items:
                    product = Product.objects.get(id=int(item))
                    OrderItem.objects.create(order=order, product=product, count=1)
            else: order = None
        form = OrderForm(instance=order)
        addresses = customer.addresses.all()
        items = []
        for item in order.items.all():
            items.append((OrderItemForm(instance=item), item))
        resp = render(request, "order/cart.html", {
            'order': order, 'form': form, 'addresses': addresses, 'items': items, 'msgs': msgs,
        })
        resp.set_cookie("cart", '')
        return resp

    def post(self, request, *args, **kwargs):
        try: customer = Customer.objects.get(id=request.user.id)
        except Customer.DoesNotExist: return redirect(reverse("customer:logout"))
        order = customer.orders.filter(status='U')[0]
        order.address = Address.objects.get(id=int(request.POST["address"]))
        form = OrderForm(request.POST)
        if form.is_valid():
            order.code = request.POST["code"] or None
            order.save()
            data, code = order.readable_final_price, 1
        else:
            order.code = None
            order.save()
            data, code = form.errors['__all__'].as_data()[0].messages[0], 0
        return JsonResponse({'code': code, 'data': data})


class ChangeItemView(LoginRequiredMixin, View):
    """
    View for Return Form Order Item Check Validated Change Count
    """

    def post(self, request, *args, **kwargs):
        item = OrderItem.objects.get(id=request.GET['item'])
        form = OrderItemForm(request.POST)
        if form.is_valid():
            item.count = request.POST["count"]
            item.save()
            code, data = 1, {
                'total': item.order.readable_total_price,
                'final': item.order.readable_final_price,
            }
        else:
            key = 'count' if request.POST["count"] == '0' else '__all__'
            code, data = 0, form.errors[key].as_data()[0].messages[0]
        return JsonResponse({'code': code, 'data': data, 'count': item.count})


class RemoveItemView(LoginRequiredMixin, View):
    """
    View for Remove an Item from Basket Cart by Logical Delete
    """

    def get(self, request, *args, **kwargs):
        try: customer = Customer.objects.get(id=request.user.id)
        except Customer.DoesNotExist: return redirect(reverse("customer:logout"))
        item = OrderItem.objects.get(id=request.GET['item'])
        if item.order.customer == customer: item.delete()
        return redirect(reverse("order:cart"))


class OrdersCustomerView(LoginRequiredMixin, generic.ListView):
    """
    Show History of Orders List for Customer Can Filter by Status
    """

    context_object_name = "orders"
    template_name = "order/orders.html"

    def get_queryset(self):
        try: customer = Customer.objects.get(id=self.request.user.id)
        except Customer.DoesNotExist: return redirect(reverse("customer:logout"))
        result = customer.orders.exclude(status__exact='U').order_by("-id")
        kwargs = self.request.GET
        if "status" in kwargs:
            result = result.filter(status__exact=kwargs["status"])
        return result


class ChangeCartStatusView(LoginRequiredMixin, View):
    """
    View for Change Status of Order to Paid or Canceling
    """

    def get(self, request, *args, **kwargs):
        try: customer = Customer.objects.get(id=request.user.id)
        except Customer.DoesNotExist: return redirect(reverse("customer:logout"))
        order = customer.orders.get(id=request.GET['order'])
        if order.customer == customer:
            if request.GET['status'] == 'P':
                order.payment()
                order.save()
            if request.GET['status'] == 'C':
                order.cancel()
                order.save()
        return redirect(reverse("order:orders"))
