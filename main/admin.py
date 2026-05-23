from django.contrib import admin
from .models import *

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "balance",
        "interest_balance",
        "referral_profit"
    )

@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "deposit_type",
        "amount_usd",
        "status",
        "created_at"
    )

@admin.register(Withdraw)
class WithdrawAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "withdraw_type",
        "amount_usd",
        "status",
        "created_at"
    )

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "type",
        "amount",
        "status",
        "created_at"
    )

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "message",
        "is_read",
        "created_at"
    )

@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "sender",
        "message",
        "created_at"
    )

@admin.register(ReferralBonus)
class ReferralBonusAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "referrer",
        "referred_user",
        "bonus_percent",
        "is_active"
    )