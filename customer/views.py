from django.shortcuts import render
from django.views import generic

from .forms import *

# Create your views here.
class CustomerRegisterView(generic.FormView):
    """
    Generic Class Based View for Register New Customer
    """

    form_class = CustomerForm
    template_name = "customer/register.html"
    success_url = 'https://google.com'

    def form_valid(self, form):
        form.save()
        return "https://google.com"
