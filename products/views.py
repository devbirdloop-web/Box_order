from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Box
from .forms import BoxForm


def product_list(request):
    boxes = Box.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'products/product_list.html', {'boxes': boxes})


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.role != 'admin':
            return redirect('user_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@admin_required
def manage_products(request):
    boxes = Box.objects.all().order_by('-created_at')
    return render(request, 'products/manage_products.html', {'boxes': boxes})


@login_required
@admin_required
def add_product(request):
    if request.method == "POST":
        form = BoxForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_products')
    else:
        form = BoxForm()

    return render(request, 'products/product_form.html', {
        'form': form,
        'title': 'Add Product'
    })


@login_required
@admin_required
def edit_product(request, pk):
    box = get_object_or_404(Box, pk=pk)

    if request.method == "POST":
        form = BoxForm(request.POST, request.FILES, instance=box)
        if form.is_valid():
            form.save()
            return redirect('manage_products')
    else:
        form = BoxForm(instance=box)

    return render(request, 'products/product_form.html', {
        'form': form,
        'title': 'Edit Product'
    })


@login_required
@admin_required
def delete_product(request, pk):
    box = get_object_or_404(Box, pk=pk)

    if request.method == "POST":
        box.delete()
        return redirect('manage_products')

    return render(request, 'products/delete_product.html', {'box': box})