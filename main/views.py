from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
import random
import string

from .models import (
    Profile,
    Deposit,
    Withdraw,
    Transaction,
    Notification,
    SupportMessage,
    ReferralBonus
)


# =========================================
# GENERATE REFERRAL CODE
# =========================================
def generate_referral_code():

    return ''.join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=8
        )
    )


# =========================================
# REGISTER
# =========================================
def register(request):

    error = None

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        if password != confirm:

            error = "Passwords do not match"

        elif User.objects.filter(username=email).exists():

            error = "Email already exists"

        else:

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )

            Profile.objects.create(
                user=user,
                referral_code=generate_referral_code()
            )

            return redirect("/login/")

    return render(request, "register.html", {
        "error": error
    })


# =========================================
# LOGIN
# =========================================
def login_view(request):

    error = None

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user:

            login(request, user)

            return redirect("/dashboard/")

        else:

            error = "Invalid credentials"

    return render(request, "login.html", {
        "error": error
    })


# =========================================
# DASHBOARD
# =========================================
@login_required
def dashboard(request):

    profile = Profile.objects.get(
        user=request.user
    )

    referral_bonuses = ReferralBonus.objects.filter(
        referrer=request.user
    ).order_by("-id")

    active_bonus = 0
    locked_bonus = 0

    now = timezone.now()

    for bonus in referral_bonuses:

        if bonus.expires_at > now:

            active_bonus += float(
                bonus.bonus_percent
            )

        else:

            locked_bonus += float(
                bonus.bonus_percent
            )

    total_daily_percent = 5 + active_bonus

    unread_messages = SupportMessage.objects.filter(
        user=request.user,
        sender="admin",
        is_read=False
    ).count()

    referral_link = (
        request.build_absolute_uri("/register/")
        + f"?ref={profile.referral_code}"
    )

    recent_transactions = Transaction.objects.filter(
        user=request.user
    ).order_by("-id")[:10]

    total_referrals = ReferralBonus.objects.filter(
        referrer=request.user
    ).count()

    return render(request, "dashboard.html", {

        "profile": profile,

        "active_bonus_percent":
        round(active_bonus, 2),

        "locked_bonus_percent":
        round(locked_bonus, 2),

        "total_daily_percent":
        round(total_daily_percent, 2),

        "referral_bonuses":
        referral_bonuses,

        "referral_link":
        referral_link,

        "total_referrals":
        total_referrals,

        "referral_profit":
        profile.referral_profit,

        "unread_messages":
        unread_messages,

        "recent_transactions": recent_transactions,
    })


# =========================================
# CLAIM INTEREST
# =========================================
@login_required
def claim_interest(request):

    profile = Profile.objects.get(
        user=request.user
    )

    profile.balance += profile.interest_balance

    Transaction.objects.create(
        user=request.user,
        type="Interest",
        amount=profile.interest_balance
    )

    profile.interest_balance = 0

    profile.save()

    return JsonResponse({
        "balance": float(profile.balance),
        "interest": float(profile.interest_balance)
    })


# =========================================
# DEPOSIT
# =========================================
@login_required
def deposit(request):

    rate = 1400

    if request.method == "POST":

        deposit_type = request.POST.get("type")

        amount_usd = 0

        if deposit_type == "MTN":

            amount_rwf = float(
                request.POST.get("amount_rwf")
            )

            amount_usd = amount_rwf / rate

            Deposit.objects.create(

                user=request.user,

                deposit_type=deposit_type,

                amount_usd=amount_usd,

                amount_rwf=amount_rwf,

                phone=request.POST.get("phone"),

                names=request.POST.get("names")
            )

        else:

            amount_usd = float(
                request.POST.get("amount_usdt")
            )

            Deposit.objects.create(

                user=request.user,

                deposit_type=deposit_type,

                amount_usd=amount_usd,

                wallet=request.POST.get("wallet")
            )

        Notification.objects.create(
            user=request.user,
            message="Deposit request submitted"
        )

        return redirect("/dashboard/")

    return render(request, "deposit.html", {
        "rate": rate
    })


# =========================================
# WITHDRAW
# =========================================
@login_required
def withdraw(request):

    rate = 1400

    if request.method == "POST":

        withdraw_type = request.POST.get("type")

        amount = float(
            request.POST.get("amount_usd")
        )

        Withdraw.objects.create(

            user=request.user,

            withdraw_type=withdraw_type,

            amount_usd=amount,

            phone=request.POST.get("phone"),

            id_names=request.POST.get("id_names"),

            wallet=request.POST.get("wallet")
        )

        Notification.objects.create(
            user=request.user,
            message="Withdraw request submitted"
        )

        return redirect("/dashboard/")

    return render(request, "withdraw.html", {
        "rate": rate
    })


# =========================================
# TRANSACTIONS
# =========================================
@login_required
def transactions(request):

    transactions = Transaction.objects.filter(
        user=request.user
    ).order_by("-id")

    return render(request, "transactions.html", {
        "transactions": transactions
    })


# =========================================
# NOTIFICATIONS
# =========================================
@login_required
def notifications(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-id")

    return render(request, "notifications.html", {
        "notifications": notifications
    })


# =========================================
# SUPPORT
# =========================================
@login_required
def support(request):

    if request.method == "POST":

        message = request.POST.get("message")

        SupportMessage.objects.create(
            user=request.user,
            sender="user",
            message=message
        )

        return redirect("/support/")

    messages = SupportMessage.objects.filter(
        user=request.user
    ).order_by("id")

    return render(request, "support.html", {
        "messages": messages
    })


# =========================================
# LOGOUT
# =========================================
@login_required
def logout_view(request):

    logout(request)

    return redirect("/login/")