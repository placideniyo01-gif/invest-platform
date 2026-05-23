from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# =========================================
# PROFILE
# =========================================
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

    last_interest_update = models.DateTimeField(
        default=timezone.now
    )

    referral_code = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    referred_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="referrals"
    )

    def __str__(self):
        return self.user.username


# =========================================
# DEPOSIT
# =========================================
class Deposit(models.Model):

    STATUS = (
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    deposit_type = models.CharField(
        max_length=20
    )

    amount_usd = models.DecimalField(
        max_digits=20,
        decimal_places=6,
        default=0
    )

    amount_rwf = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    names = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    wallet = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - ${self.amount_usd}"


# =========================================
# WITHDRAW
# =========================================
class Withdraw(models.Model):

    STATUS = (
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    withdraw_type = models.CharField(
        max_length=20
    )

    amount_usd = models.DecimalField(
        max_digits=20,
        decimal_places=6
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    id_names = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    wallet = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - ${self.amount_usd}"


# =========================================
# TRANSACTION
# =========================================
class Transaction(models.Model):

    TYPE = (
        ("Deposit", "Deposit"),
        ("Withdraw", "Withdraw"),
        ("Interest", "Interest"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    type = models.CharField(
        max_length=20,
        choices=TYPE
    )

    amount = models.DecimalField(
        max_digits=20,
        decimal_places=6
    )

    status = models.CharField(
        max_length=20,
        default="Success"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.type}"


# =========================================
# NOTIFICATION
# =========================================
class Notification(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.message


# =========================================
# REFERRAL BONUS
# =========================================
class ReferralBonus(models.Model):

    referrer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="referrer_bonus"
    )


    deposit = models.ForeignKey(
        Deposit,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    bonus_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.1
    )

    expires_at = models.DateTimeField()

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.referrer.username} bonus"


# =========================================
# SUPPORT CHAT
# =========================================
class SupportMessage(models.Model):

    SENDER_CHOICES = (
        ("user", "User"),
        ("admin", "Admin"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    sender = models.CharField(
        max_length=10,
        choices=SENDER_CHOICES,
        default="user"
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    is_typing = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.sender}"