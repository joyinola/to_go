from django.db import models
from django.contrib.auth import get_user_model

from multiselectfield import MultiSelectField
# Create your models here.

"""
active
pending
decline
accepted

"""
User = get_user_model()

def upload_license(instance,filename):
    return f'to_go/{instance.user.first_name}/document/{filename}'

def upload_vehicle_pic(instance,filename):
    return f'to_go/plate_no/{instance.plate_no}/document/{filename}'
def upload_doc(instance,filename):
    pass

# class Days(models.Model):
#     day = models.CharField(max_length=8)



class vehicle(models.Model):
    # rider = models.ForeignKey(rider, on_delete=models.SET_NULL, null = True, blank = True)
    picture = models.ImageField(upload_to=upload_vehicle_pic,null=True,blank=True)
    type = models.CharField(max_length=125)
    brand = models.CharField(max_length=125)
    plate_no = models.CharField(max_length=125,unique = True)
    seat_cap = models.IntegerField()



class account(models.Model):
    account_type = models.CharField(max_length=10)
    account_number = models.CharField(max_length=125)
    back_code = models.CharField(max_length=4)
    currency = models.CharField(max_length=4)
    recipient_code = models.CharField(max_length = 50)

class rider(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null = True, blank = True)
    vehicle = models.ForeignKey(vehicle, on_delete=models.SET_NULL, null = True, blank = True)
    account = models.OneToOneField(account, on_delete=models.SET_NULL,null=True,blank=True)
    route_from = models.CharField(max_length=125)
    route_to = models.CharField(max_length=125)
    bus_stop = models.CharField(max_length=125)
    licence = models.FileField(upload_to=upload_license,null=True,blank=True)
    price = models.CharField(max_length=20)
    # account = models.OneToOneField(account, null=True,blank=True,on_delete=models.SET_NULL)
    # work_days = models.JSONField()
    # open_time = models.TimeField()
    # close_time = models.TimeField()