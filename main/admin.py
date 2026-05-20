from django.contrib import admin
from django.utils.html import format_html

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

    search_fields = (
        'user__username',
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
        'show_contact',
        "names",
        'status',
        'approve_button',
        'reject_button',
        'created_at'
    )

    list_filter = (
        'status',
        'deposit_type'
    )

    search_fields = (
        'user__username',
        'phone',
        'wallet'
    )

    def show_contact(self, obj):

        if obj.deposit_type == "MTN":
            return obj.phone

        return obj.wallet

    show_contact.short_description = "Phone / Wallet"

    def approve_button(self, obj):

        if obj.status == "Pending":

            return format_html(

                '<a style="background:green;color:white;padding:5px 10px;border-radius:5px;text-decoration:none;" href="/approve-deposit/{}/">Approve</a>',

                obj.id
            )

        return "Approved"

    def reject_button(self, obj):

        if obj.status == "Pending":

            return format_html(

                '<a style="background:red;color:white;padding:5px 10px;border-radius:5px;text-decoration:none;" href="/reject-deposit/{}/">Reject</a>',

                obj.id
            )

        return "-"


# =========================
# WITHDRAW ADMIN
# =========================
@admin.register(Withdraw)
class WithdrawAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'withdraw_type',
        'amount_usd',
        'display_destination',
        'id_names',
        'status',
        'approve_button',
        'reject_button',
        'created_at'
    )

    list_filter = (
        'status',
        'withdraw_type'
    )

    search_fields = (
        'user__username',
        'phone',
        'wallet'
    )

    def display_destination(self, obj):

        if obj.withdraw_type == "MTN":
            return obj.phone

        elif obj.withdraw_type == "USDT":
            return obj.wallet

        return "-"

    display_destination.short_description = "Phone /Wallet"

    def approve_button(self, obj):

        if obj.status == "Pending":

            return format_html(

                '<a style="background:green;color:white;padding:5px 10px;border-radius:5px;text-decoration:none;" href="/approve-withdraw/{}/">Approve</a>',

                obj.id
            )

        return "Approved"

    def reject_button(self, obj):

        if obj.status == "Pending":

            return format_html(

                '<a style="background:red;color:white;padding:5px 10px;border-radius:5px;text-decoration:none;" href="/reject-withdraw/{}/">Reject</a>',

                obj.id
            )

        return "-"


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

    list_filter = (
        'type',
        'status'
    )

    search_fields = (
        'user__username',
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

    list_filter = (
        'is_read',
    )

    search_fields = (
        'user__username',
        'message'
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
        'expires_at',
        'created_at'
    )

    search_fields = (
        'referrer__username',
        'referred_user__username'
    )


# =========================
# SUPPORT CHAT ADMIN
# =========================
@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'sender',
        'short_message',
        'is_read',
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

    def short_message(self, obj):

        return obj.message[:50]

    short_message.short_description = "Message"