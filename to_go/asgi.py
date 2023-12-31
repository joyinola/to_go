"""
ASGI config for to_go project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""


import os

from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()

from chat.middleware.user_auth_middleware import UserAuthMiddleware
from channels.routing import ProtocolTypeRouter,URLRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "to_go.settings")

import chat.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": UserAuthMiddleware(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    )
 
})

# web: daphne to_go.asgi:application --port $PORT --bind 0.0.0.0 -v2

# worker: python manage.py runworker channel_layer -v2
 