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


# =========================================
# ADMIN TITLES
# =========================================
admin.site.site_header = "Invest Platform Admin"
admin.site.site_title = "Invest Platform"
admin.site.index_title = "Admin Dashboard"


# =========================================
# PROFILE ADMIN
# =========================================
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


# =========================================
# DEPOSIT ADMIN
# =========================================
@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'deposit_type',
        'amount_usd',
        'show_contact',
        'names',
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
                '<a style="background:green;color:white;padding:6px 12px;border-radius:6px;text-decoration:none;" href="/approve-deposit/{}/">Approve</a>',
                obj.id
            )

        return format_html(
            '<span style="color:green;font-weight:bold;">Approved</span>'
        )

    approve_button.short_description = "Approve"

    def reject_button(self, obj):

        if obj.status == "Pending":

            return format_html(
                '<a style="background:red;color:white;padding:6px 12px;border-radius:6px;text-decoration:none;" href="/reject-deposit/{}/">Reject</a>',
                obj.id
            )

        return "-"

    reject_button.short_description = "Reject"


# =========================================
# WITHDRAW ADMIN
# =========================================
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

        return obj.wallet

    display_destination.short_description = "Phone / Wallet"

    def approve_button(self, obj):

        if obj.status == "Pending":

            return format_html(
                '<a style="background:green;color:white;padding:6px 12px;border-radius:6px;text-decoration:none;" href="/approve-withdraw/{}/">Approve</a>',
                obj.id
            )

        return format_html(
            '<span style="color:green;font-weight:bold;">Approved</span>'
        )

    approve_button.short_description = "Approve"

    def reject_button(self, obj):

        if obj.status == "Pending":

            return format_html(
                '<a style="background:red;color:white;padding:6px 12px;border-radius:6px;text-decoration:none;" href="/reject-withdraw/{}/">Reject</a>',
                obj.id
            )

        return "-"

    reject_button.short_description = "Reject"


# =========================================
# TRANSACTION ADMIN
# =========================================
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


# =========================================
# NOTIFICATION ADMIN
# =========================================
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


# =========================================
# REFERRAL BONUS ADMIN
# =========================================
@admin.register(ReferralBonus)
class ReferralBonusAdmin(admin.ModelAdmin):

    list_display = (
        'referrer',
        'referred_user',
        'bonus_percent',
        'is_active_display',
        'expires_at',
        'created_at'
    )

    search_fields = (
        'referrer__username',
        'referred_user__username'
    )

    def is_active_display(self, obj):

        if obj.is_active:

            return format_html(
                '<span style="background:green;color:white;padding:5px 10px;border-radius:10px;">ACTIVE</span>'
            )

        return format_html(
            '<span style="background:orange;color:white;padding:5px 10px;border-radius:10px;">EXPIRED</span>'
        )

    is_active_display.short_description = "Status"


# =========================================
# SUPPORT MESSAGE ADMIN
# =========================================
@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'sender_badge',
        'short_message',
        'message_status',
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

    ordering = (
        '-created_at',
    )

    def short_message(self, obj):

        return obj.message[:60]

    short_message.short_description = "Message"

    def sender_badge(self, obj):

        if obj.sender == "admin":

            return format_html(
                '<span style="background:#2563eb;color:white;padding:5px 10px;border-radius:10px;font-weight:bold;">ADMIN</span>'
            )

        return format_html(
            '<span style="background:#22c55e;color:white;padding:5px 10px;border-radius:10px;font-weight:bold;">USER</span>'
        )

    sender_badge.short_description = "Sender"

    def message_status(self, obj):

        if not obj.is_read and obj.sender == "user":

            return format_html(
                '<span style="background:red;color:white;padding:5px 10px;border-radius:10px;font-weight:bold;">NEW MESSAGE</span>'
            )

        return format_html(
            '<span style="background:green;color:white;padding:5px 10px;border-radius:10px;">READ</span>'
        )

    message_status.short_description = "Status"

    def save_model(
        self,
        request,
        obj,
        form,
        change
    ):

        obj.is_read = True

        super().save_model(
            request,
            obj,
            form,
            change
        )