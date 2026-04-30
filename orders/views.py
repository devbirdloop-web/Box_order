from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Box
from .cart import Cart
from .models import Order, OrderItem





# -------------------------
# Orders Home
# -------------------------
def orders(request):
    return HttpResponse("Orders Page")


# -------------------------
# CART VIEW
# -------------------------
def cart_view(request):
    cart = Cart(request)

    return render(request, 'orders/cart.html', {
        'cart': cart.cart,
        'total': cart.total()
    })


# -------------------------
# ADD TO CART
# -------------------------
def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Box, id=product_id)

    cart.add(product)
    return redirect('cart')


# -------------------------
# REMOVE FROM CART
# -------------------------
def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Box, id=product_id)

    cart.remove(product)
    return redirect('cart')


# -------------------------
# UPDATE CART
# -------------------------
def update_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Box, id=product_id)

    qty = request.POST.get('qty')
    cart.update(product, qty)

    return redirect('cart')


# -------------------------
# CHECKOUT
# -------------------------
@login_required
def checkout(request):
    cart = Cart(request)

    if not cart.cart:
        return redirect('cart')

    order = Order.objects.create(user=request.user)
    total = 0

    for pid, item in cart.cart.items():
        product = Box.objects.get(id=pid)

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=item['qty'],
            price=item['price']
        )

        total += item['price'] * item['qty']

    order.total_price = total
    order.save()

    cart.clear()

    return render(request, 'orders/success.html', {'order': order})


# -------------------------
# MY ORDERS
# -------------------------
@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)

    return render(request, 'orders/my_orders.html', {
        'orders': orders
    })
    
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
def admin_orders(request):
    orders = Order.objects.select_related('user').prefetch_related('items__product').order_by('-created_at')
    return render(request, 'orders/admin_orders.html', {'orders': orders})


@login_required
@admin_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        status = request.POST.get("status")
        if status in ['pending', 'processing', 'delivered']:
            order.status = status
            order.save()

    return redirect('admin_orders')

@login_required
def my_orders(request):
    orders = (
        Order.objects
        .filter(user=request.user)
        .prefetch_related('items__product')
        .order_by('-created_at')
    )

    return render(request, 'orders/my_orders.html', {
        'orders': orders
    })