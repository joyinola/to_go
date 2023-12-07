from django.urls import path
from .views import ListChatView, MessageView

urlpatterns = [
    path("list_user_chat/", ListChatView.as_view(), name="list-chat"),
    path("chat_messages/", MessageView.as_view(), name="msg_view"),
]
