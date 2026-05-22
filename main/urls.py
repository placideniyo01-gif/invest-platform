# main/urls.py

from django.urls import path
from .views import *

urlpatterns = [

    path(
        "register/",
        register_view
    ),

    path(
        "login/",
        login_view
    ),

    path(
        "logout/",
        logout_view
    ),

    path(
        "dashboard/",
        dashboard
    ),

    path(
        "deposit/",
        deposit
    ),

    path(
        "withdraw/",
        withdraw
    ),

    path(
        "support/",
        support
    ),

    path(
        "notifications/",
        notifications
    ),

    path(
        "transactions/",
        transactions
    ),

    path(
        "claim-interest/",
        claim_interest
    ),
]