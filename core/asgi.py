# core/asgi.py

import os

from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from channels.auth import AuthMiddlewareStack

from django.core.asgi import get_asgi_application

import main.routing

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'core.settings'
)

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({

    "http":django_asgi_app,

    "websocket":AuthMiddlewareStack(

        URLRouter(
            main.routing.websocket_urlpatterns
        )
    ),
})