from django.shortcuts import render, redirect, get_object_or_404
from django.views import View, generic
from django.urls import reverse, reverse_lazy

from .models import *

# Create your views here.
class ProductsListView(generic.ListView):
    """
    Generic Class Based View for Show List of All Active Products Item
    """

    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        result = Product.objects.all()
        kwargs = self.request.GET
        if "category" in kwargs:
            result = result.filter(category__slug=kwargs["category"])
        if "brand" in kwargs:
            result = result.filter(brand__slug=kwargs["brand"])
        return result


class ProductDetailView(generic.DetailView):
    """
    Generic Class Based View for Show Detail of a Product Item
    """

    model = Product
    context_object_name = "product"
