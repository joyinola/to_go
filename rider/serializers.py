from rest_framework import serializers
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from .models import rider,vehicle
from .utils import send_otp

User = get_user_model()

class VehicleSerializer(serializers.ModelSerializer):
     class Meta:
          model = vehicle
          fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
     
     class Meta:
          model = User
          fields = ['first_name', 'last_name', 'email','is_verified',]
class RiderSerializer(serializers.ModelSerializer):

    

    email = serializers.EmailField(write_only=True, required=True)
    car_pic = serializers.ImageField(write_only=True, required=True)
    license = serializers.FileField(write_only = True)
    car_type = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(write_only=True, required=True)
    last_name =  serializers.CharField(write_only=True, required=True)
    seat_cap = serializers.IntegerField(write_only=True, required=True)
    brand = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    plate_no = serializers.CharField(write_only=True, required=True)

    # route_from = serializers.CharField(write_only=True, required=True)
    # otp = serializers.CharField(write_only=False, read_only=False)

    class Meta:
        model = rider
        fields = [ 
             
                'route_from',
                'route_to',
                'bus_stop',
                'license',
                'price',
                  'first_name',
                  'last_name',
                  'car_type',
                  'car_pic',
                  'seat_cap',
                  'brand',
                  'password',
                  'plate_no',
                  'email',
                  

                  ]
     

    def create (self,validated_data):
        
        email = validated_data.get('email',None)
        
        try:
            user_obj = User.objects.create(
            email = email) 

        except IntegrityError:
        
            raise serializers.ValidationError('User already exists')


        user_obj.first_name = validated_data.get('first_name',None)
        user_obj.last_name = validated_data.get('last_name',None)
        user_obj.set_password(validated_data.get('password',None))
        user_obj.save()

        
        # print('user_id',user_obj)

        vehicle_obj = vehicle.objects.create(
                picture = validated_data.get('car_pic',None),
                type = validated_data.get('car_type',None),
                brand = validated_data.get('brand',None),
                plate_no = validated_data.get('plate_no',None),
                seat_cap = validated_data.get('seat_cap', None )
        )
        vehicle_obj.save()

        
        rider_obj = rider.objects.create(
            user = user_obj,
            vehicle = vehicle_obj,
            route_from = validated_data.get('route_from',None),
            route_to = validated_data.get('route_to',None),
            bus_stop = validated_data.get('bus_stop',None),
            licence = validated_data.get('license',None),
            price = validated_data.get('price',None)

            )
        rider_obj.save()
        
        
        
        

        return rider_obj

class RequestPassswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

