import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db import IntegrityError
from django.db.models import Q


from account.models import User
from .models import Messages, Chat


class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # get current user and other user from url params

        current_user_id = self.scope["user"].id

        # if self.scope['user'].id else int(self.scope['query_string'])
        other_user_id = self.scope["url_route"]["kwargs"]["other_user_id"]

        """ room name for user 1 and 2 will be 2_1, it has to be the same room name for both user 1 and 2 so they can interect in the room """
        self.room_name = (
            f"{current_user_id}_{other_user_id}"
            if int(current_user_id) > int(other_user_id)
            else f"{other_user_id}_{current_user_id}"
        )
        self.room_group_name = f"chat_{self.room_name}"
        # Accept Conection
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group

        await self.channel_layer.group_discard(self.room_group_name, self.channel_layer)
        await self.disconnect(close_code)

        # Close the websocket connection
        await self.close()

    # Receive message from WebSocket
    async def receive(self, text_data):
        # Deserialize the JSON data
        text_data_json = json.loads(text_data)
        content = text_data_json["message"]
        sender_id = self.scope["user"].id
        receiver_id = other_user_id = self.scope["url_route"]["kwargs"]["other_user_id"]

        # Save Chat to the Database
        chat_message = await self.saveMessage(
            content, sender_id, receiver_id, self.room_name
        )

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": chat_message,
            },
        )

        # Add a field for the read status and update it based on the received message
        # You can use Django models to interact with the database

    @database_sync_to_async
    def saveMessage(self, content, sender_id, receiver_id, room_name):
        sender = User.objects.get(id=sender_id)
        receiver = User.objects.get(id=receiver_id)

        # get chat with sender and receiver

        chat_room_exist = Chat.objects.filter(
            Q(user_1=sender, user_2=receiver) | Q(user_1=receiver, user_2=sender)
        )
        if chat_room_exist:
            chat_room = chat_room_exist[0]

        else:
            chat_room = Chat.objects.create(user_1=sender, user_2=receiver)

        # try:
        #     chat_room,is_created = Chat.objects.get_or_create(user_1 = sender, user_2 = receiver)

        # except IntegrityError:
        #     chat_room,is_created = Chat.objects.get_or_create(user_1 = receiver, user_2 = sender)

        message_obj = Messages.objects.create(
            chat=chat_room,
            sender=sender,
            message=content,
        )
        return {
            "action": "message",
            "sender": str(sender),
            "content": content,
            "room_name": room_name,
            # 'is_read': str(message_obj.is_read),
            "created": str(message_obj.created_at),
        }

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
