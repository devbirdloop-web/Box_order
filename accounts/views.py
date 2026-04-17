from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

@never_cache
@login_required
def home(request):
    return render(request, "dashboard/home.html")

User = get_user_model()

# SIGNUP

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm_password")

        # validations
        if password != confirm:
            return render(request, "accounts/signup.html", {"error": "Passwords do not match"})

        if User.objects.filter(username=username).exists():
            return render(request, "accounts/signup.html", {"error": "Username already exists"})

        if User.objects.filter(email=email).exists():
            return render(request, "accounts/signup.html", {"error": "Email already registered"})

        # create user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            full_name=full_name,
            mobile=mobile,
            address=address
        )

        login(request, user)
        return redirect("home")

    return render(request, "accounts/signup.html")


# LOGIN

from django.contrib.auth import logout

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")   # ✅ don't logout

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "accounts/login.html", {"error": "Invalid credentials"})

    return render(request, "accounts/login.html")


# LOGOUT
def logout_view(request):
    logout(request)
    return redirect("login")