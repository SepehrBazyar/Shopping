from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import MessageForm

# Create your views here.
@csrf_exempt
def send_message(request):
    if request.method == 'GET':
        form = MessageForm()
        return render(request, "landing/contact.html", {
            'form': form
        })

    if request.method == 'POST':
        print(request.POST)
        return HttpResponse("OK!")
