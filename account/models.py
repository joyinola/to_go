from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

# from rideshare.models import card_detail,account,vehicle

# User = get_user_model()

# def upload_data(instance,filename):
#     return f'to_go/{instance.user.first_name}_{instance.user.last_name}_{instance.user.id}/document/{filename}'

# def upload_vehicle_pic(instance,filename):
#     return f'to_go/plate_no/{instance.plate_no}/document/{filename}'

"""
Contains User model and models native to the rides 
"""

"""Custome User model with no ussername and
         authenticates with email or phone number"""

class UserManager(BaseUserManager):
    def _create_user(self,email,password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None,  **extra_fields):
        user = self._create_user(email,password, **extra_fields)
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None,  **extra_fields):
    
        user = self._create_user(email,password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,PermissionsMixin):
    user_type = [
        ('rider','rider'),
        ('passenger','passenger')
    ]
    is_staff = models.BooleanField(default=False)
    username = None
    email = models.CharField(max_length=125, unique=True)
    phone_no = models.CharField(max_length=125)
    first_name = models.CharField(max_length=125)
    last_name = models.CharField(max_length=125)
    created_at = models.DateTimeField(auto_now_add=True)
    otp = models.CharField(max_length=10,null = True, blank = True)
    is_verified = models.BooleanField(default=False)
    user_type = models.CharField(choices=user_type, max_length=10)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

# class passenger(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE,null = True, blank = True)
#     card = models.ForeignKey(card_detail, on_delete=models.SET_NULL,blank = True,null = True)
#     picture = models.ImageField(upload_to=upload_data,null=True,blank=True)

# class rider(models.Model):
#     user = models.OneToOneField(User, on_delete=models.SET_NULL, null = True, blank = True)
#     picture = models.ImageField(upload_to=upload_data,null=True,blank=True)
#     vehicle = models.ForeignKey(vehicle, on_delete=models.SET_NULL, null = True, blank = True)
#     account = models.OneToOneField(account, on_delete=models.SET_NULL,null=True,blank=True)
#     route_from = models.CharField(max_length=125)
#     route_to = models.CharField(max_length=125)
#     bus_stop = models.CharField(max_length=125)
#     licence = models.FileField(upload_to=upload_data,null=True,blank=True)
#     price = models.CharField(max_length=20)
#     # account = models.OneToOneField

# class vehicle(models.Model):
#     rider = models.ForeignKey(rider, on_delete=models.SET_NULL, null = True, blank = True)
#     picture = models.ImageField(upload_to=upload_vehicle_pic,null=True,blank=True)
#     type = models.CharField(max_length=125)
#     brand = models.CharField(max_length=125)
#     plate_no = models.CharField(max_length=125)
#     seat_cap = models.IntegerField()
 
