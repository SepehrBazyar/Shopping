from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import JsonResponse
from django.views import View, generic
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.utils.translation import get_language, gettext_lazy as _

from .models import *
from landing.forms import SearchForm

# Create your views here.
class ProductsListView(generic.ListView):
    """
    Generic Class Based View for Show List of All Active Products Item
    """

    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        result = Product.objects.all()
        kwargs = self.request.GET
        if "category" in kwargs:
            result = result.filter(category__slug=kwargs["category"])
        if "brand" in kwargs:
            result = result.filter(brand__slug=kwargs["brand"])
        if "search" in kwargs:
            form = SearchForm(kwargs)
            if form.is_valid():
                text = form.cleaned_data['search']
                result = result.filter(Q(slug__icontains=text)|
                    Q(title_en__icontains=text) | Q(title_fa__icontains=text) |
                    Q(category__title_en__icontains=text) | Q(category__title_fa__icontains=text) | 
                    Q(brand__title_en__icontains=text) | Q(brand__title_fa__icontains=text) | 
                    Q(category__slug__icontains=text) | Q(brand__slug__icontains=text)
                )
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'slides': Product.objects.exclude(image='Unknown.jpg').order_by('?')[:3],
            'form': SearchForm(),
        })
        if get_language() == 'en': context['prev'], context['next'] = "prev", "next"
        else: context['prev'], context['next'] = "next", "prev"
        return context


class ProductDetailView(generic.DetailView):
    """
    Generic Class Based View for Show Detail of a Product Item
    """

    model = Product
    context_object_name = "product"

    def post(self, request, *args, **kwargs):
        resp = JsonResponse({'msg': _("Product Item has Successfully been Added to the Cart")})
        cart = request.COOKIES.get("cart", "")
        resp.set_cookie("cart", cart + request.POST["product"] + ',')
        return resp


class CategoryListView(generic.ListView):
    """
    Generic Class Based View for Show List of All Categories in Collapsed Cards
    """

    context_object_name = "parents"

    def get_queryset(self):
        parents = Category.objects.filter(root=None)
        return parents

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if get_language() == 'en': context['Right'], context['Left'] = "Right", "Left"
        else: context['Right'], context['Left'] = "Left", "Right"
        return context
