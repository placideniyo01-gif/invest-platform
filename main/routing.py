# main/routing.py

from django.urls import re_path
from .consumers import *

websocket_urlpatterns = [

    re_path(
        r'ws/balance/$',
        BalanceConsumer.as_asgi()
    ),

    re_path(
        r'ws/support/$',
        SupportConsumer.as_asgi()
    ),
]