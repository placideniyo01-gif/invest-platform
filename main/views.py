# main/models.py

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    balance = models.DecimalField(
        max_digits=20,
        decimal_places=6,
        default=0
    )

    interest_balance = models.DecimalField(
        max_digits=20,
        decimal_places=6,
        default=0
    )

    referral_profit = models.DecimalField(
        max_digits=20,
        decimal_places=6,
        default=0
    )

    def __str__(self):
        return self.user.username


class Deposit(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    type = models.CharField(
        max_length=20
    )

    amount_usd = models.DecimalField(
        max_digits=20,
        decimal_places=6
    )

    status = models.CharField(
        max_length=20,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class Withdraw(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    type = models.CharField(
        max_length=20
    )

    amount = models.DecimalField(
        max_digits=20,
        decimal_places=6
    )

    status = models.CharField(
        max_length=20,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class Transaction(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    type = models.CharField(
        max_length=100
    )

    amount = models.DecimalField(
        max_digits=20,
        decimal_places=6
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class Notification(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class SupportMessage(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    sender = models.CharField(
        max_length=20
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class ReferralBonus(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    referred_user = models.ForeignKey(
        User,
        related_name="referred_user",
        on_delete=models.CASCADE
    )

    deposit = models.ForeignKey(
        Deposit,
        on_delete=models.CASCADE
    )

    bonus_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    expires_at = models.DateTimeField()

    is_active = models.BooleanField(
        default=True
    )