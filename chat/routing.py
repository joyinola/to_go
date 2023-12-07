from django.urls import path, re_path

from .consumer import MessageConsumer

websocket_urlpatterns = [
    # re_path(r'ws/chat/(?P<room_id>\w+)/$', consumers.MessageConsumer.as_asgi()),
    path("ws/chat/<int:other_user_id>/", MessageConsumer.as_asgi()),
]
