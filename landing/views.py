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
        if form.is_valid(): print(form.cleaned_data)
        else: msg, status = _("Please be Careful & Try Again..."), 400
        return HttpResponse(msg, status=status)
