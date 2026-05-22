from django.urls import path
from . import views

urlpatterns = [

    path("", views.dashboard, name="dashboard"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register, name="register"),

    path("deposit/", views.deposit, name="deposit"),
    path("withdraw/", views.withdraw, name="withdraw"),

    path("transactions/", views.transactions, name="transactions"),
    path("notifications/", views.notifications, name="notifications"),

    path("support/", views.support, name="support"),

    path("claim-interest/", views.claim_interest, name="claim_interest"),
]