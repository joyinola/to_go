# from django.db import models
# from rideshare.models import User
# # Create your models here.

# class Chat(models.Model):
#   user_1 = models.ForeignKey(User, on_delete=models.CASCADE)
#   user_2 = models.ForeignKey(User, on_delete=models.CASCADE)

    
# class Messages(models.Model):
#     chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
#     sender = models.ForeignKey(User,on_delete=models.SET_NULL )
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     # unread = models.BooleanField(default=False)
#     class Meta:
#         ordering = ['created_at']