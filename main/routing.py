from django.urls import path
from .consumers import BalanceConsumer

websocket_urlpatterns = [

    path(
        "ws/balance/",
        BalanceConsumer.as_asgi()
    ),
]