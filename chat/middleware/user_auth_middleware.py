import os
import jwt


from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from account.models import User

class UserAuthMiddleware:
    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        token = False
        query = scope["query_string"]

        if query:
            query = query.decode()

        if query:
            query = query.split("=")
            if query[0] == "token":
                token = query[1]

        if token:
            # jwt token let's decode it
            tokenData = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
            # save it on user scope
            scope["user"] = await self.get_user(tokenData)

        return await self.app(scope, receive, send)

    @database_sync_to_async
    def get_user(self, data):
        user = User.objects.get(email=data.get("user_id"))
        return user
