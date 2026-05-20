from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# =========================
# PROFILE
# =========================
class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    balance = models.FloatField(default=0)

    interest_balance = models.FloatField(default=0)

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


# =========================
# DEPOSIT
# =========================
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
        max_length=10
    )

    amount_usd = models.FloatField(default=0)

    amount_rwf = models.FloatField(default=0)

    phone = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    names = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    wallet = models.CharField(
        max_length=200,
        null=True,
        blank=True
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

        return f"{self.user} - ${self.amount_usd}"


# =========================
# WITHDRAW
# =========================
class Withdraw(models.Model):

    STATUS = (
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    withdraw_type = models.CharField(
        max_length=10
    )

    amount_usd = models.FloatField()

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

        return f"{self.user} - ${self.amount_usd}"


# =========================
# TRANSACTIONS
# =========================
class Transaction(models.Model):

    TYPE = (
        ("Deposit", "Deposit"),
        ("Withdraw", "Withdraw"),
        ("Interest", "Interest"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    type = models.CharField(
        max_length=20,
        choices=TYPE
    )

    amount = models.FloatField()

    status = models.CharField(
        max_length=20,
        default="Success"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user} - {self.type}"


# =========================
# NOTIFICATIONS
# =========================
class Notification(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    message = models.CharField(
        max_length=255
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.message


# =========================
# REFERRAL BONUS
# =========================
class ReferralBonus(models.Model):

    referrer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="referrer_bonus"
    )

    referred_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="referred_bonus"
    )

    deposit = models.ForeignKey(
        Deposit,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    bonus_percent = models.FloatField(
        default=0.1
    )

    expires_at = models.DateTimeField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

# =========================
# SUPPORT CHAT
# =========================
class SupportMessage(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    sender = models.CharField(
        max_length=20,
        choices=(
            ("user", "user"),
            ("admin", "admin"),
        )
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user} - {self.sender}"
        
    @property
    def is_active(self):

        return timezone.now() < self.expires_at

    def __str__(self):

        return f"{self.referrer} earned {self.bonus_percent}%"