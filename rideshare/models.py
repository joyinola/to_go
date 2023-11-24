from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.contrib.auth import get_user_model
# from account.models import rider
# from rider.models import rider
# Create your models here.

User = get_user_model()

def upload_data(instance,filename):
    return f'to_go/{instance.user.first_name}_{instance.user.last_name}_{instance.user.id}/document/{filename}'

def upload_vehicle_pic(instance,filename):
    # get_rider = rider.objects.get(vehicle=instance)
    # get_rider = rider.objects.get(user = get_user)
    return f'to_go/plate_no/{instance.plate_no}/document/{filename}'


# class card_detail(models.Model):
#     card_no = models.CharField(max_length=125)
#     expiry_date =models.CharField(max_length=10)
#     cvv = models.CharField(max_length=3)
    
# class vehicle(models.Model):
#     # rider = models.ForeignKey(rider, on_delete=models.SET_NULL, null = True, blank = True)
#     picture = models.ImageField(upload_to=upload_vehicle_pic,null=True,blank=True)
#     type = models.CharField(max_length=125)
#     brand = models.CharField(max_length=125)
#     plate_no = models.CharField(max_length=125)
#     seat_cap = models.IntegerField()



class passenger(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null = True, blank = True)
    # card = models.ForeignKey(card_detail, on_delete=models.SET_NULL,blank = True,null = True)
    # picture = models.ImageField(upload_to=upload_data,null=True,blank=True)

class vehicle(models.Model):
    # rider = models.ForeignKey(rider, on_delete=models.SET_NULL, null = True, blank = True)
    choices = [
        ("Car","Car"),
        ("Bus","Bus"),
        ("Tricycle","Tricycle"),
        ("Motocycle", "Motorcycle")
    ]
    picture = models.ImageField(upload_to=upload_vehicle_pic,null=True,blank=True)
    type = models.CharField(choices = choices, max_length=10)
    brand = models.CharField(max_length=125)
    plate_no = models.CharField(max_length=125)
    seat_cap = models.IntegerField()
    # seat_available = models.IntegerField(blank = True, null =True)

    @property
    def seat_available(self):
        rider_ = rider.objects.get(vehicle=self)
        pending_orders = Order.objects.filter(rider = rider_, passenger_order_status = 'Accepted').count()
        return int(self.seat_cap)-int(pending_orders)

class AccountDetail(models.Model):
    account_type = models.CharField(max_length=10)
    account_name = models.CharField(max_length = 255)
    account_number = models.CharField(max_length=125)
    back_code = models.CharField(max_length=4)
    currency = models.CharField(max_length=4)
    recipient_code = models.CharField(max_length = 50)     

class rider(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null = True, blank = True,related_name='rider')
    # picture = models.ImageField(upload_to=upload_data,null=True,blank=True)
    vehicle = models.ForeignKey(vehicle, on_delete=models.SET_NULL, null = True, blank = True,related_name='rider')
    account = models.OneToOneField(AccountDetail, on_delete=models.SET_NULL,null=True,blank=True, related_name = 'rider')
    route_from = models.CharField(max_length=125)
    route_to = models.CharField(max_length=125)
    trip_duration = models.CharField(max_length=10)
    bus_stop = models.CharField(max_length=125)
    licence = models.FileField(upload_to=upload_data,null=True,blank=True)
    price = models.IntegerField()
    is_active = models.BooleanField(default=False)
    # account = models.OneToOneField(AccountDetail,on_delete=models.SET_NULL,null=True,blank=True)

class Trip(models.Model):

    rider_status = [

        ("Accepted","Accepted"),
        ("On Transit","On Transit"),
        ("Completed","Completed"),
        ("Cancelled","Cancelled")
    ]
    # orders = models.JSONField()
    passengers = models.ForeignKey(passenger,on_delete=models.SET_NULL,blank=True,null=True)
    # passenger_count = models.IntegerField(default=0)
    rider = models.OneToOneField(rider, on_delete=models.CASCADE)
    rider_order_status = models.CharField(choices = rider_status, null=True, blank=True,max_length=10)
    created_at =models.DateField(auto_now_add=True)

    @property
    def passenger_count(self):
        return Order.objects.filter(trip = self.id, rider_order_status='Accepted').count()



class Order(models.Model):

    rider_order_status = [
        ("Accepted","Accepted"),  
        # ("On Transit","On Transit"),
        # ("Completed","Completed"),
        ("Declined","Declined")
    ]

    passenger_order_status = [

        ("Accepted","Accepted"),  
        ("On Transit","On Transit"),
        ("Completed","Completed"),
        ("Cancelled","Cancelled")
    ]

    rider = models.ForeignKey(rider, on_delete=models.CASCADE)
    passenger = models.ForeignKey(passenger, on_delete=models.CASCADE,related_name='orders')
    reference = models.CharField(max_length=20,blank=True,null=True)
    order_datetime =models.DateTimeField(auto_now=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, null = True, blank = True,related_name='order')
    has_paid = models.BooleanField(default=False)
    passenger_order_status = models.CharField(choices = passenger_order_status, default = 'Accepted', max_length=10)
    rider_order_status = models.CharField(choices = rider_order_status,max_length=10, null = True,blank=True)
    # seat_available = models.IntegerField()

