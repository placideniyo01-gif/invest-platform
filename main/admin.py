from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.contrib.auth.models import User

from .models import (
    Profile,
    Deposit,
    Withdraw,
    Transaction,
    Notification,
    ReferralBonus,
    SupportMessage
)


# =========================
# PROFILE ADMIN
# =========================
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'balance',
        'interest_balance',
        'referred_by'
    )


# =========================
# DEPOSIT ADMIN
# =========================
@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'deposit_type',
        'amount_usd',
        'status',
        'created_at'
    )


# =========================
# WITHDRAW ADMIN
# =========================
@admin.register(Withdraw)
class WithdrawAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'withdraw_type',
        'amount_usd',
        'status',
        'created_at'
    )


# =========================
# TRANSACTION ADMIN
# =========================
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'type',
        'amount',
        'status',
        'created_at'
    )


# =========================
# NOTIFICATION ADMIN
# =========================
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'message',
        'is_read',
        'created_at'
    )


# =========================
# REFERRAL BONUS ADMIN
# =========================
@admin.register(ReferralBonus)
class ReferralBonusAdmin(admin.ModelAdmin):

    list_display = (
        'referrer',
        'referred_user',
        'bonus_percent',
        'expires_at'
    )


# =========================
# SUPPORT MESSAGE ADMIN
# =========================
@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'sender',
        'short_message',
        'is_read',
        'reply_button',
        'created_at'
    )

    list_filter = (
        'sender',
        'is_read'
    )

    search_fields = (
        'user__username',
        'message'
    )

    # =====================
    # SHORT MESSAGE
    # =====================
    def short_message(self, obj):

        return obj.message[:50]

    short_message.short_description = "Message"

    # =====================
    # REPLY BUTTON
    # =====================
    def reply_button(self, obj):

        return format_html(

            '<a style="background:#2563eb;color:white;padding:6px 12px;border-radius:8px;text-decoration:none;" href="/admin/main/supportmessage/reply/{}/">Reply</a>',

            obj.user.id
        )

    reply_button.short_description = "Reply"

    # =====================
    # CUSTOM URLS
    # =====================
    def get_urls(self):

        urls = super().get_urls()

        custom_urls = [

            path(
                'reply/<int:user_id>/',
                self.admin_site.admin_view(
                    self.reply_view
                ),
                name='reply-support'
            ),

        ]

        return custom_urls + urls

    # =====================
    # REPLY VIEW
    # =====================
    def reply_view(self, request, user_id):

        user = User.objects.get(id=user_id)

        if request.method == "POST":

            message = request.POST.get("message")

            if message:

                SupportMessage.objects.create(

                    user=user,
                    sender="admin",
                    message=message,
                    is_read=False
                )

                return redirect(
                    f"/admin/main/supportmessage/reply/{user.id}/"
                )

        chats = SupportMessage.objects.filter(
            user=user
        ).order_by("created_at")

        csrf_token = get_token(request)

        html = f"""

        <html>

        <head>

            <title>Support Reply</title>

            <style>

                body{{
                    background:#0f172a;
                    color:white;
                    font-family:Arial;
                    padding:30px;
                }}

                .chat{{
                    max-width:700px;
                    margin:auto;
                }}

                .msg{{
                    padding:15px;
                    border-radius:12px;
                    margin-bottom:15px;
                }}

                .user{{
                    background:#1e293b;
                }}

                .admin{{
                    background:#2563eb;
                }}

                textarea{{
                    width:100%;
                    height:120px;
                    border:none;
                    border-radius:10px;
                    padding:15px;
                    margin-top:20px;
                }}

                button{{
                    margin-top:15px;
                    background:#22c55e;
                    color:white;
                    border:none;
                    padding:15px 25px;
                    border-radius:10px;
                    cursor:pointer;
                }}

            </style>

        </head>

        <body>

        <div class="chat">

        <h1>Support Chat - {user.username}</h1>

        """

        for chat in chats:

            html += f"""

            <div class="msg {chat.sender}">

                <strong>{chat.sender.upper()}</strong>

                <br><br>

                {chat.message}

            </div>

            """

        html += f"""

        <form method="POST">

            <input
                type="hidden"
                name="csrfmiddlewaretoken"
                value="{csrf_token}"
            >

            <textarea
                name="message"
                placeholder="Write reply..."
            ></textarea>

            <button type="submit">
                Send Reply
            </button>

        </form>

        </div>

        </body>
        </html>

        """

        return HttpResponse(html)