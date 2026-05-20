from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from datetime import timedelta
import requests

from .utils import *
from .models import (
    Profile,
    Deposit,
    Withdraw,
    Transaction,
    Notification,
    ReferralBonus
)


# =========================
# UPDATE INTEREST
# =========================
def update_interest(profile):

    now = timezone.now()

    seconds_passed = (
        now - profile.last_interest_update
    ).total_seconds()

    if seconds_passed <= 0:
        return

    # BASE %
    total_percent = 5.0

    # ACTIVE REFERRALS
    active_bonuses = ReferralBonus.objects.filter(
        referrer=profile.user,
        expires_at__gt=now
    )

    active_bonus_percent = 0

    for bonus in active_bonuses:

        active_bonus_percent += float(
            bonus.bonus_percent
        )

    # EXTRA BONUS EVERY 10 USERS
    total_referrals = active_bonuses.count()

    groups_of_10 = total_referrals // 10

    extra_group_bonus = groups_of_10 * 0.5

    total_percent += active_bonus_percent
    total_percent += extra_group_bonus

    # CALCULATE
    daily_interest = (
        profile.balance * total_percent
    ) / 100

    per_second = daily_interest / 86400

    earned = per_second * seconds_passed

    profile.interest_balance += earned

    profile.last_interest_update = now

    profile.save()


# =========================
# LIVE RATE
# =========================
def get_live_rate():

    try:

        r = requests.get(
            "https://api.exchangerate-api.com/v4/latest/USD"
        )

        data = r.json()

        return float(
            data["rates"]["RWF"]
        )

    except:

        return 1400


# =========================
# LOGIN
# =========================
def login_view(request):

    error = ""

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:

            error = "Fill all fields"

        else:

            user = authenticate(
                request,
                username=email,
                password=password
            )

            if user is not None:

                login(request, user)

                return redirect("dashboard")

            else:

                error = "Invalid email or password"

    return render(request, "login.html", {
        "error": error
    })

# =========================
# REGISTER
# =========================
def register_view(request):

    error = ""

    ref_code = request.GET.get("ref")

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        # CHECK EMPTY FIELDS
        if not email or not password or not confirm:

            error = "Fill all fields"

        # PASSWORD MATCH
        elif password != confirm:

            error = "Passwords do not match"

        # USER EXISTS
        elif User.objects.filter(
            username=email
        ).exists():

            error = "Email already exists"

        else:

            try:

                # CREATE USER
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password
                )

                # REFERRER
                referrer = None

                if ref_code:

                    try:

                        referrer = User.objects.get(
                            id=ref_code
                        )

                    except:
                        pass

                # CREATE PROFILE
                Profile.objects.create(
                    user=user,
                    referred_by=referrer
                )

                # AUTO LOGIN
                login(request, user)

                return redirect("dashboard")

            except Exception as e:

                error = str(e)

    return render(request, "register.html", {
        "error": error
    })
# =========================
# DASHBOARD
# =========================
@login_required
def dashboard(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    update_interest(profile)

    referral_bonuses = ReferralBonus.objects.filter(
        referrer=request.user
    ).order_by("-created_at")

    active_bonus_percent = 0
    locked_bonus_percent = 0

    for bonus in referral_bonuses:

        if bonus.is_active:

            active_bonus_percent += float(
                bonus.bonus_percent
            )

        else:

            locked_bonus_percent += float(
                bonus.bonus_percent
            )

    total_referrals = referral_bonuses.count()

    groups_of_10 = total_referrals // 10

    extra_group_bonus = (
        groups_of_10 * 0.5
    )

    total_daily_percent = (
        5 +
        active_bonus_percent +
        extra_group_bonus
    )

    referral_profit = round(
        (
            profile.balance *
            (active_bonus_percent / 100)
        ),
        4
    )

    referral_link = request.build_absolute_uri(
        f"/register/?ref={request.user.id}"
    )

    context = {

        "profile": profile,

        "referral_bonuses": referral_bonuses,

        "active_bonus_percent": round(
            active_bonus_percent,
            2
        ),

        "locked_bonus_percent": round(
            locked_bonus_percent,
            2
        ),

        "extra_group_bonus": round(
            extra_group_bonus,
            2
        ),

        "total_referrals": total_referrals,

        "referral_profit": referral_profit,

        "total_daily_percent": round(
            total_daily_percent,
            2
        ),

        "referral_link": referral_link
    }

    return render(
        request,
        "dashboard.html",
        context
    )


# =========================
# CLAIM INTEREST
# =========================
@login_required
def claim_interest(request):

    profile = Profile.objects.get(
        user=request.user
    )

    update_interest(profile)

    profile.balance += (
        profile.interest_balance
    )

    profile.interest_balance = 0

    profile.save()

    Notification.objects.create(
        user=request.user,
        message="Interest claimed successfully"
    )

    push_balance_update(
        request.user,
        profile
    )

    return JsonResponse({

        "balance": profile.balance,

        "interest": profile.interest_balance
    })


# =========================
# DEPOSIT
# =========================
@login_required
def deposit(request):

    rate = get_live_rate()

    display_rate = rate + (
        rate * 0.03
    )

    profile = Profile.objects.get(
        user=request.user
    )

    if request.method == "POST":

        deposit_type = request.POST.get("type")

        # MTN
        if deposit_type == "MTN":

            amount_rwf = float(
                request.POST.get(
                    "amount_rwf",
                    0
                )
            )

            amount_usd = (
                amount_rwf / display_rate
            )

            if amount_usd < 20:

                return JsonResponse({
                    "error":
                    "Minimum deposit is $20"
                })

            Deposit.objects.create(

                user=request.user,

                deposit_type="MTN",

                amount_rwf=amount_rwf,

                amount_usd=amount_usd,

                phone=request.POST.get(
                    "phone"
                ),

                names=request.POST.get(
                    "names"
                ),

                status="Pending"
            )

            Transaction.objects.create(

                user=request.user,

                type="Deposit",

                amount=amount_usd
            )

        # USDT
        else:

            amount_usdt = float(
                request.POST.get(
                    "amount_usdt",
                    0
                )
            )

            if amount_usdt < 20:

                return JsonResponse({
                    "error":
                    "Minimum deposit is $20"
                })

            Deposit.objects.create(

                user=request.user,

                deposit_type="USDT",

                amount_usd=amount_usdt,

                wallet=request.POST.get(
                    "wallet"
                ),

                status="Pending"
            )

            Transaction.objects.create(

                user=request.user,

                type="Deposit",

                amount=amount_usdt
            )

        return redirect("dashboard")

    return render(
        request,
        "deposit.html",
        {
            "rate": round(
                display_rate,
                2
            ),
            "profile": profile
        }
    )


# =========================
# WITHDRAW
# =========================
@login_required
def withdraw(request):

    rate = get_live_rate()

    display_rate = rate - (
        rate * 0.02
    )

    profile = Profile.objects.get(
        user=request.user
    )

    if request.method == "POST":

        amount_usd = float(
            request.POST.get(
                "amount_usd",
                0
            )
        )

        if amount_usd > profile.balance:

            return JsonResponse({
                "error":
                "Insufficient balance"
            })

        withdraw_type = request.POST.get(
            "type"
        )

        if withdraw_type == "MTN":

            Withdraw.objects.create(

                user=request.user,

                withdraw_type="MTN",

                amount_usd=amount_usd,

                phone=request.POST.get(
                    "phone"
                ),

                id_names=request.POST.get(
                    "id_names"
                ),

                status="Pending"
            )

        else:

            Withdraw.objects.create(

                user=request.user,

                withdraw_type="USDT",

                amount_usd=amount_usd,

                wallet=request.POST.get(
                    "wallet"
                ),

                status="Pending"
            )

        return redirect("dashboard")

    return render(
        request,
        "withdraw.html",
        {
            "rate": round(
                display_rate,
                2
            )
        }
    )


# =========================
# TRANSACTIONS
# =========================
@login_required
def transactions_view(request):

    transactions = Transaction.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "transactions.html",
        {
            "transactions": transactions
        }
    )


# =========================
# NOTIFICATIONS
# =========================
@login_required
def notifications_view(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "notifications.html",
        {
            "notifications": notifications
        }
    )


# =========================
# BALANCE API
# =========================
@login_required
def balance_api(request):

    profile = Profile.objects.get(
        user=request.user
    )

    update_interest(profile)

    return JsonResponse({

        "balance":
        profile.balance,

        "interest":
        profile.interest_balance
    })


# =========================
# PUSH LIVE BALANCE
# =========================
def push_balance_update(
    user,
    profile
):

    channel_layer = get_channel_layer()

    if channel_layer is None:
        return

    async_to_sync(
        channel_layer.group_send
    )(
        f"user_{user.id}",
        {
            "type": "send_balance",
            "balance": float(
                profile.balance
            ),
            "interest": float(
                profile.interest_balance
            )
        }
    )


# =========================
# APPROVE DEPOSIT
# =========================
def approve_deposit(request, id):

    d = Deposit.objects.get(id=id)

    if d.status == "Pending":

        profile = Profile.objects.get(
            user=d.user
        )

        update_interest(profile)

        profile.balance += d.amount_usd

        profile.save()

        d.status = "Approved"

        d.save()

        # FIRST APPROVED DEPOSIT
        first_deposit = Deposit.objects.filter(
            user=d.user,
            status="Approved"
        ).count() == 1

        if first_deposit:

            referred_profile = Profile.objects.get(
                user=d.user
            )

            if referred_profile.referred_by:

                referrer = (
                    referred_profile.referred_by
                )

                bonus_percent = 0.1

                if d.amount_usd >= 250:
                    bonus_percent = 0.2

                if d.amount_usd >= 500:
                    bonus_percent = 0.3

                ReferralBonus.objects.create(

                    referrer=referrer,

                    referred_user=d.user,

                    deposit=d,

                    bonus_percent=bonus_percent,

                    expires_at=(
                        timezone.now() +
                        timedelta(days=30)
                    )
                )

                Notification.objects.create(

                    user=referrer,

                    message=(
                        f"You received "
                        f"+{bonus_percent}% "
                        f"bonus from "
                        f"{d.user.username}"
                    )
                )

        Notification.objects.create(

            user=d.user,

            message=(
                f"Deposit of "
                f"${d.amount_usd} approved"
            )
        )

        push_balance_update(
            d.user,
            profile
        )

    return redirect(
        "/admin/main/deposit/"
    )

# =========================
# REJECT DEPOSIT
# =========================
def reject_deposit(request, id):

    d = Deposit.objects.get(id=id)

    d.status = "Rejected"

    d.save()

    Notification.objects.create(
        user=d.user,
        message=f"Deposit of ${d.amount_usd} rejected"
    )

    return redirect('/admin/main/deposit/')


# =========================
# APPROVE WITHDRAW
# =========================
def approve_withdraw(request, id):

    w = Withdraw.objects.get(id=id)

    if w.status == "Pending":

        profile = Profile.objects.get(
            user=w.user
        )

        update_interest(profile)

        profile.balance -= w.amount_usd

        profile.save()

        w.status = "Approved"

        w.save()

        Notification.objects.create(
            user=w.user,
            message=f"Withdraw of ${w.amount_usd} approved"
        )

        push_balance_update(
            w.user,
            profile
        )

    return redirect('/admin/main/withdraw/')


# =========================
# REJECT WITHDRAW
# =========================
def reject_withdraw(request, id):

    w = Withdraw.objects.get(id=id)

    w.status = "Rejected"

    w.save()

    Notification.objects.create(
        user=w.user,
        message=f"Withdraw of ${w.amount_usd} rejected"
    )

    return redirect('/admin/main/withdraw/')


# =========================
# APPROVE DEPOSIT API
# =========================
def approve_deposit_api(request, id):

    d = Deposit.objects.get(id=id)

    if d.status == "Pending":

        profile = Profile.objects.get(
            user=d.user
        )

        profile.balance += d.amount_usd

        profile.save()

        d.status = "Approved"

        d.save()

        return JsonResponse({
            "message": "Approved successfully"
        })

    return JsonResponse({
        "message": "Already processed"
    })