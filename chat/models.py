# from django.db import models
# from rideshare.models import User
# # Create your models here.

# class Chat(models.Model):
#     account_owner =  models.OneToOneField(User, on_delete=models.SET_NULL)
#     chat_name = models.OneToOneField(User, on_delete=models.SET_NULL)


    
# class Messages(models.Model):
#     chat = models.OneToOneField(Chat, on_delete=models.CASCADE)
#     sender = models.OneToOneField(User,on_delete=models.SET_NULL )
#     receiver = models.OneToOneField(User, on_delete=models.SET_NULL)
#     text = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['created_at']