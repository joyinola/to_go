from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .serializers import ChatSerializer, MessageSerializer
from .models import Chat, Messages


from django.db.models import Q

"""
list of chat -- people who has a chat history with you, each chat has messages 
"""


class ListChatView(ListAPIView):
    serializer_class = ChatSerializer

    def list(self, request, *args, **kwargs):
        queryset = Chat.objects.filter(Q(user_1=request.user) | Q(user_2=request.user))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(
                page, many=True, context={"user_id": request.user}
            )
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
            queryset, many=True, context={"user_id": request.user}
        )
        return Response(serializer.data)


class MessageView(ListAPIView):
    serializer_class = MessageSerializer

    def list(self, request, *args, **kwargs):
        queryset = Messages.objects.filter(chat=request.GET.get("chat_id"))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(
                page, many=True, context={"user_id": request.user}
            )
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
            queryset, many=True, context={"user_id": request.user}
        )

        return Response(serializer.data)
