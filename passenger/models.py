from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

class card(models.Model):
    card_no = models.CharField(max_length=125)
    expiry_date =models.CharField(max_length=10)
    cvv = models.CharField(max_length=3)
    
class passenger(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    card = models.OneToOneField(card, on_delete=models.SET_NULL,blank = True,null = True)
