from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views import generic

from .models import Customer
from .forms import *

# Create your views here.
class CustomerLoginView(LoginView):
    """
    Customize Built-in View for Login Customers
    """
    
    authentication_form = CustomerLoginForm
    template_name = "customer/login.html"


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

    def form_valid(self, form):
        Customer.objects.create_user(username=form.data["username"],
                                    password=form.data["password1"])
        return redirect(reverse("product:categories"))
