from django.contrib import auth
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views import generic, View

from .models import Customer
from .forms import *

# Create your views here.
class CustomerLoginView(LoginView):
    """
    Customize Built-in View for Login Customers
    """
    
    authentication_form = CustomerLoginForm
    template_name = "customer/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("product:categories"))
        return super().get(request, *args, **kwargs)


class CustomerLogoutView(LogoutView):
    """
    Customize Built-in View for Logout Customers
    """

    pass


class CustomerRegisterView(generic.FormView):
    """
    Generic Class Based View for Register New Customer
    """

    form_class = CustomerRegisterForm
    template_name = "customer/register.html"
    success_url = reverse_lazy("product:categories")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("product:categories"))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = Customer.objects.create_user(username=form.data["username"],
                                            password=form.data["password1"])
        login(self.request, user)
        return redirect(reverse("product:categories"))


class CustomerProfileView(LoginRequiredMixin, View):
    """
    View for Customer See Profile Detials and Edit it
    """

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(id=request.user.id)
        return render(request, "customer/profile.html", {
            'customer': customer,
        })


class CreateNewAddressView(LoginRequiredMixin, View):
    """
    Authenticated Customer Can Add New Address for Orders in this View
    """

    def get(self, request, *args, **kwargs):
        form = AdderssForm()
        return render(request, "customer/address.html", {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = AdderssForm(request.POST)
        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.customer = Customer.objects.get(id=request.user.id)
            new_address.save()
            return redirect(reverse("product:categories"))
        else:
            return render(request, "customer/address.html", {
            'form': form
        })
