# main/admin.py

from django.contrib import admin
from .models import *

admin.site.register(Profile)
admin.site.register(Deposit)
admin.site.register(Withdraw)
admin.site.register(Transaction)
admin.site.register(Notification)
admin.site.register(SupportMessage)
admin.site.register(ReferralBonus)