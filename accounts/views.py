from urllib import request

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages

User = get_user_model()


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        mobile = request.POST.get("mobile", "").strip()
        address = request.POST.get("address", "").strip()
        role = request.POST.get("role", "user").strip()
        password = request.POST.get("password", "")
        confirm = request.POST.get("confirm_password", "")

        if password != confirm:
            return render(request, "accounts/signup.html", {
                "error": "Passwords do not match"
            })

        if User.objects.filter(username=username).exists():
            return render(request, "accounts/signup.html", {
                "error": "Username already exists"
            })

        if User.objects.filter(email=email).exists():
            return render(request, "accounts/signup.html", {
                "error": "Email already registered"
            })

        if role not in ["admin", "user"]:
            return render(request, "accounts/signup.html", {
                "error": "Invalid role selected"
            })

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            full_name=full_name,
            mobile=mobile,
            address=address,
            role=role,
        )
        

        messages.success(request, "Account created successfully!")
        return redirect("signup")
    return render(request, "accounts/signup.html")


def login_view(request):
    if request.user.is_authenticated:
        if request.user.role == 'admin':
            return redirect('admin_dashboard')
        return redirect('user_dashboard')

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            if user.role == 'admin':
                return redirect('admin_dashboard')
            return redirect('user_dashboard')

        return render(request, "accounts/login.html", {
            "error": "Invalid credentials"
        })

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


from orders.models import Order
from products.models import Box

@never_cache
@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('user_dashboard')

    context = {
        'total_products': Box.objects.count(),
        'total_orders': Order.objects.count(),
        'pending_orders': Order.objects.filter(status='pending').count(),
        'delivered_orders': Order.objects.filter(status='delivered').count(),
    }
    return render(request, "dashboard/admin_dashboard.html", context)


@never_cache
@login_required
def user_dashboard(request):
    if request.user.role != 'user':
        return redirect('admin_dashboard')

    user_orders = Order.objects.filter(user=request.user)
    context = {
        'total_orders': user_orders.count(),
        'pending_orders': user_orders.filter(status='pending').count(),
        'delivered_orders': user_orders.filter(status='delivered').count(),
    }
    return render(request, "dashboard/user_dashboard.html", context)