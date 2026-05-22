from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Profile, Deposit, Withdraw, Transaction, Notification, SupportMessage, ReferralBonus
from django.utils import timezone


# =========================
# REGISTER
# =========================
def register(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        if password != confirm:
            return render(request, "register.html", {"error": "Passwords do not match"})

        if User.objects.filter(username=email).exists():
            return render(request, "register.html", {"error": "User already exists"})

        user = User.objects.create_user(username=email, email=email, password=password)
        Profile.objects.create(user=user)

        return redirect("login")

    return render(request, "register.html")


# =========================
# LOGIN
# =========================
def login_view(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")


# =========================
# DASHBOARD
# =========================
def dashboard(request):

    profile = Profile.objects.get(user=request.user)

    referral_bonuses = ReferralBonus.objects.filter(referrer=request.user)

    context = {
        "profile": profile,
        "referral_bonuses": referral_bonuses,
        "total_referrals": referral_bonuses.count(),
        "active_bonus_percent": 0,
        "locked_bonus_percent": 0,
        "referral_profit": profile.referral_profit,
        "referral_link": f"http://127.0.0.1:8000/register/?ref={profile.id}",
        "unread_messages": 0
    }

    return render(request, "dashboard.html", context)


# =========================
# DEPOSIT
# =========================
def deposit(request):

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

        return redirect("dashboard")

    return render(request, "deposit.html", {"rate": 1300})


# =========================
# WITHDRAW
# =========================
def withdraw(request):

    if request.method == "POST":

        Withdraw.objects.create(
            user=request.user,
            withdraw_type=request.POST.get("type"),
            amount_usd=request.POST.get("amount_usd"),
            phone=request.POST.get("phone"),
            id_names=request.POST.get("id_names"),
            wallet=request.POST.get("wallet"),
        )

        return redirect("dashboard")

    return render(request, "withdraw.html", {"rate": 1300})


# =========================
# TRANSACTIONS
# =========================
def transactions(request):

    data = Transaction.objects.filter(user=request.user)

    return render(request, "transactions.html", {"transactions": data})


# =========================
# NOTIFICATIONS
# =========================
def notifications(request):

    data = Notification.objects.filter(user=request.user)

    return render(request, "notifications.html", {"notifications": data})


# =========================
# SUPPORT
# =========================
def support(request):

    if request.method == "POST":

        SupportMessage.objects.create(
            user=request.user,
            sender="user",
            message=request.POST.get("message")
        )

        return redirect("support")

    messages = SupportMessage.objects.filter(user=request.user)

    return render(request, "support.html", {"messages": messages})


# =========================
# CLAIM INTEREST (AJAX)
# =========================
from django.http import JsonResponse

def claim_interest(request):

    profile = Profile.objects.get(user=request.user)

    profile.balance += profile.interest_balance
    profile.interest_balance = 0
    profile.save()

    return JsonResponse({
        "balance": float(profile.balance),
        "interest": float(profile.interest_balance)
    })