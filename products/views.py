from django.shortcuts import render
from .models import Box

def product_list(request):
    boxes = Box.objects.all()
    return render(request, 'products/product_list.html', {'boxes': boxes})