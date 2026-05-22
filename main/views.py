from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Profile, Deposit, Withdraw, Transaction, Notification, SupportMessage


# =========================
# LOGIN
# =========================
def login_view(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=email)
        except:
            return render(request, "login.html", {"error": "User not found"})

        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            return redirect("/dashboard/")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")


# =========================
# REGISTER
# =========================
def register_view(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        if password != confirm:
            return render(request, "register.html", {"error": "Passwords do not match"})

        if User.objects.filter(username=email).exists():
            return render(request, "register.html", {"error": "User already exists"})

        user = User.objects.create_user(username=email, password=password)
        Profile.objects.create(user=user)

        return redirect("/login/")

    return render(request, "register.html")


# =========================
# DASHBOARD
# =========================
def dashboard_view(request):

    profile = Profile.objects.get(user=request.user)

    notifications = Notification.objects.filter(user=request.user).order_by("-created_at")[:5]

    context = {
        "profile": profile,
        "notifications": notifications,
    }

    return render(request, "dashboard.html", context)


# =========================
# DEPOSIT
# =========================
def deposit_view(request):

    rate = 1200  # example rate

    if request.method == "POST":

        Deposit.objects.create(
            user=request.user,
            deposit_type=request.POST.get("type"),
            amount_usd=request.POST.get("amount_usd") or 0,
            amount_rwf=request.POST.get("amount_rwf") or 0,
            phone=request.POST.get("phone"),
            names=request.POST.get("names"),
            wallet=request.POST.get("wallet"),
        )

        return redirect("/dashboard/")

    return render(request, "deposit.html", {"rate": rate})


# =========================
# WITHDRAW
# =========================
def withdraw_view(request):

    rate = 1200

    if request.method == "POST":

        Withdraw.objects.create(
            user=request.user,
            withdraw_type=request.POST.get("type"),
            amount_usd=request.POST.get("amount_usd"),
            phone=request.POST.get("phone"),
            id_names=request.POST.get("id_names"),
            wallet=request.POST.get("wallet"),
        )

        return redirect("/dashboard/")

    return render(request, "withdraw.html", {"rate": rate})


# =========================
# SUPPORT
# =========================
def support_view(request):

    messages = SupportMessage.objects.filter(user=request.user)

    if request.method == "POST":

        SupportMessage.objects.create(
            user=request.user,
            sender="user",
            message=request.POST.get("message")
        )

        return redirect("/support/")

    return render(request, "support.html", {"messages": messages})


# =========================
# NOTIFICATIONS
# =========================
def notifications_view(request):

    notifications = Notification.objects.filter(user=request.user)

    return render(request, "notifications.html", {
        "notifications": notifications
    })


# =========================
# TRANSACTIONS
# =========================
def transactions_view(request):

    transactions = Transaction.objects.filter(user=request.user)

    return render(request, "transactions.html", {
        "transactions": transactions
    })