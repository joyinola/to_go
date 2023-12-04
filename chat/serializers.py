# from rest_framework import serializers
# from django.contrib.auth import get_user_model

# from rideshare.serializers import UserSerializer
# from .models import Chat, Messages

# User = get_user_model()
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'first_name']

# class ChatSerializer(serializers.ModelSerializer):
#     other_user = serializers.SerializerMethodField()
#     last_message = serializers.SerializerMethodField()
#     # unread_msg = serializers.SerializerMethodField()
#     class Meta:
#         model = Chat
#         fields = ['other_user', 'last_message']

#     def get_other_user(self,obj):
#         request_user = self.context.get('user_id')
#         if request_user.id == obj.user_1:
#             return UserSerializer(obj.user_1).data
        
#         return UserSerializer(obj.user_2).data
    
#     def get_last_message(self,obj):
#         last_msg = Messages.objects.filter(chat = obj).last()
#         return last_msg.message

#     # def get_other_user(self,obj,context):
#     #     pass

