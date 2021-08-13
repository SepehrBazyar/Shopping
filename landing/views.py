from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext_lazy as _

from product.views import ProductsListView, CategoryListView
from customer.views import CustomerLoginView, CustomerProfileView, CustomerRegisterView
from order.views import BasketCartView
from .forms import MessageForm

# Create your views here.
def page_not_found(request, exception):
    """
    Handling My Custom 404 Error View Page Not Found
    """
    
    data = {}
    return render(request, "landing/404.html", data, status=404)

def send_message(request):
    """
    Function View for Show Form Model by Message & Get Text with AJAX Single Page
    """

    if request.method == 'GET':
        form = MessageForm()
        return render(request, "landing/contact.html", {
            'form': form
        })

    elif request.method == 'POST':
        msg, status = _("Your Message was Successfully Received"), 200
        form = MessageForm(request.POST)
        if form.is_valid(): form.save()
        else: msg, status = _("Please be Careful & Try Again..."), 400
        return HttpResponse(msg, status=status)

# Duplicate Page Views Import in Landing App for Easy URL Routing out of Apps
home = ProductsListView.as_view()
category = CategoryListView.as_view()
login = CustomerLoginView.as_view()
register = CustomerRegisterView.as_view()
profile = CustomerProfileView.as_view()
cart = BasketCartView.as_view()
