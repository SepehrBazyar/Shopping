from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from .models import Customer
from .forms import *

# Create your views here.
class CustomerRegisterView(generic.FormView):
    """
    Generic Class Based View for Register New Customer
    """

    form_class = CustomerForm
    template_name = "customer/register.html"
    success_url = reverse_lazy("product:categories")

    def form_valid(self, form):
        Customer.objects.create_user(username=form.data["username"],
                                    password=form.data["password1"])
        return redirect(reverse("product:categories"))
