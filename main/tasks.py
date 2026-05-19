from celery import shared_task
from .models import Profile

@shared_task
def interest_engine():

    profiles = Profile.objects.all()

    for p in profiles:
        daily = p.balance * 0.05
        per_sec = daily / 86400

        p.interest_balance += per_sec
        p.save()