from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

# Create your models here.

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
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email_or_phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(email_or_phone,password,**extra_fields)
    
    def create_superuser(self, email_or_phone,password=None,  **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        
        return self._create_user(email_or_phone,password, **extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
    username = None
    email = models.CharField(max_length=125,unique=True)
    phone_no = models.CharField(max_length=125,unique=True)
    first_name = models.CharField(max_length=125)
    last_name = models.CharField(max_length=125)
    created_at = models.DateTimeField(auto_now_add=True)
    otp = models.CharField(max_length=10,null = True, blank = True)
    # username = models.CharField(max_length=100, unique = False, null=True, default = 'user')
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

class Trips(models.Model):
    pass


    