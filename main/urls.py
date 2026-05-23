from django.urls import path
from . import views

urlpatterns = [

    path('', views.dashboard),

    path('login/', views.login_view),

    path('register/', views.register),

    path('dashboard/', views.dashboard),

    path('deposit/', views.deposit),

    path('withdraw/', views.withdraw),

    path('transactions/', views.transactions),

    path('notifications/', views.notifications),

    path('support/', views.support),

    path('claim-interest/', views.claim_interest),

    path('logout/', views.logout_view),
]