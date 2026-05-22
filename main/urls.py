from django.urls import path
from .views import *

urlpatterns = [
    path("login/", login_view),
    path("register/", register_view),
    path("dashboard/", dashboard_view),
    path("deposit/", deposit_view),
    path("withdraw/", withdraw_view),
    path("support/", support_view),
    path("notifications/", notifications_view),
    path("transactions/", transactions_view),
]