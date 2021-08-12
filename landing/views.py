from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext_lazy as _

from .forms import MessageForm

# Create your views here.
def page_not_found(request, exception):
    """
    Handling My Custom 404 Error View Page Not Found
    """
    
    data = {}
    return render(request, "landing/404.html", data)

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
        status = 400
        form = MessageForm(request.POST)
        if form.is_valid():
            status = 200
            print(form.cleaned_data)
        return HttpResponse(_("Your Message was Successfully Received"), status=200)
