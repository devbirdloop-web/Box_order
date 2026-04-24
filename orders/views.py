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