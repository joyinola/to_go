# from django.shortcuts import render
# from rest_framework.generics import ListAPIView
# from rest_framework.response import Response

# from .serializers import ChatSerializer
# from .models import Chat
# """
# list of chat -- people who has a chat history with you, each chat has messages 
# """

# class ListChatView(ListAPIView):

#     serializer_class = ChatSerializer
#     queryset = Chat.objects.all()

#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())

#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True, context = {'user_id': request.user})
#             return self.get_paginated_response(serializer.data)

#         serializer = self.get_serializer(queryset, many=True,context = {'user_id': request.user})
#         return Response(serializer.data)

    

# # class MessageView(ListAPIView):
# #     pass
