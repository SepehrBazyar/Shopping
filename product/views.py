from django.shortcuts import render, redirect, get_object_or_404
from django.views import View, generic
from django.urls import reverse, reverse_lazy

from .models import *

# Create your views here.
class ProductsListView(generic.ListView):
    """
    
    """

    model = Product
    context_object_name = "products"
    paginate_by = 10


class ProductDetailView(generic.DetailView):
    """
    
    """

    model = Product
    context_object_name = "product"
