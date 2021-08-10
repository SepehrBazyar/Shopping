from django.shortcuts import render, HttpResponse

# Create your views here.
def send_message(request):
    if request.method == 'GET':
        return render(request, "landing/contact.html")
