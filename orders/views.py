from django.http import HttpResponse

def orders(request):
    return HttpResponse("Orders Page")