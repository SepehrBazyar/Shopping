from django.contrib import auth
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
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
            return redirect(reverse("product:lists"))
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
    success_url = reverse_lazy("product:lists")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("product:lists"))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = Customer.objects.create_user(username=form.data["username"],
                                            password=form.data["password1"])
        login(self.request, user)
        return redirect(reverse("product:lists"))


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    """
    Inheritanced from Built-in View for Change Customer Password in New Template
    """

    form_class = CustomerChangePassword
    success_url = reverse_lazy("customer:profile")
    template_name = "customer/password.html"


class CustomerProfileView(LoginRequiredMixin, View):
    """
    View for Customer See Profile Detials and Edit it
    """

    def get(self, request, *args, **kwargs):
        try: customer = Customer.objects.get(id=request.user.id)
        except Customer.DoesNotExist: return redirect(reverse("customer:logout"))
        return render(request, "customer/profile.html", {
            'customer': customer,
        })


class CustomerEditProfileView(LoginRequiredMixin, View):
    """
    View for Change Customer Information Edit Name & Photo
    """

    def get(self, request, *args, **kwargs):
        try: customer = Customer.objects.get(id=request.user.id)
        except Customer.DoesNotExist: return redirect(reverse("customer:logout"))
        form = CustomerEditProfileForm(instance=customer)
        return render(request, "customer/edit.html", {
            'form': form,
        })
    
    def post(self, request, *args, **kwargs):
        try: customer = Customer.objects.get(id=request.user.id)
        except Customer.DoesNotExist: return redirect(reverse("customer:logout"))
        form = CustomerEditProfileForm(instance=customer, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse("customer:profile"))
        return render(request, "customer/edit.html", {
            'form': form,
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
            try: customer = Customer.objects.get(id=request.user.id)
            except Customer.DoesNotExist: return redirect(reverse("customer:logout"))
            new_address.customer = customer
            new_address.save()
            return redirect(reverse("customer:profile"))
        else:
            return render(request, "customer/address.html", {
            'form': form
        })


class EditAddressView(LoginRequiredMixin, View):
    """
    View for Change Written Addresses of a Customer
    """

    def get(self, request, *args, **kwargs):
        try: customer = Customer.objects.get(id=request.user.id)
        except Customer.DoesNotExist: return redirect(reverse("customer:logout"))
        address = Address.objects.get(zip_code__exact=kwargs["zip_code"])
        if address.customer == customer:
            form = AdderssForm(instance=address)
            return render(request, "customer/address.html", {
                'form': form
            })
        return redirect(reverse("customer:profile"))

    def post(self, request, *args, **kwargs):
        try: customer = Customer.objects.get(id=request.user.id)
        except Customer.DoesNotExist: return redirect(reverse("customer:logout"))
        address = Address.objects.get(zip_code__exact=kwargs["zip_code"])
        if address.customer == customer:
            form = AdderssForm(data=request.POST, instance=address)
            if form.is_valid():
                form.save()
                return redirect(reverse("customer:profile"))
            else:
                return render(request, "customer/address.html", {
                    'form': form
                })
        return redirect(reverse("customer:profile"))
