from django.urls import path
from . import views
from . import views

urlpatterns = [

    path('', views.login_view, name='login'),

    path('register/', views.register_view, name='register'),

    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('claim-interest/', views.claim_interest, name='claim_interest'),
    path('transactions/', views.transactions_view, name="transactions"),
    path('approve-deposit/<int:id>/', views.approve_deposit),
    path('reject-deposit/<int:id>/', views.reject_deposit),
    path("support/", views.support_view, name="support"),
    path('approve-withdraw/<int:id>/', views.approve_withdraw),
    path('reject-withdraw/<int:id>/', views.reject_withdraw),
    path(
    'notifications/',
    views.notifications_view,
    name='notifications'
),
    path(
    'balance-api/',
    views.balance_api,
    name='balance_api'
),
    path("api/approve-deposit/<int:id>/", views.approve_deposit_api),
]   