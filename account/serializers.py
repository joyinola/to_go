from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from rideshare.models import rider,passenger,vehicle

User = get_user_model()



class RequestPassswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class UserSerializer(serializers.ModelSerializer):
     
     class Meta:
          model = User
          fields = ['id','first_name', 'last_name', 'email','is_verified',]

class PassangerSerializier(serializers.ModelSerializer):
   
    email = serializers.EmailField(write_only=True, required=True)
    first_name = serializers.CharField(write_only=True, required=True)
    last_name =  serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    phone_no = serializers.CharField(write_only=True, required=True)
    user_picture = serializers.ImageField(write_only=True, required=True)
    
  
    
    class Meta:
        model = passenger

        fields = [
            'email',
            'password',
            'first_name',
            'last_name',
            'phone_no',
            'user_picture'
            
        ]

  
       

    def create(self,validated_data):

        # print(validated_data)

        email = validated_data.pop('email',None)
        phone_no = validated_data.pop('phone_no',None)

        #gets or create a user with the email and phone_no, raises an error if either phone or email is not unique
    
        try:
            email_obj = User.objects.get(email = email)
            user = True
        
        except:
            user= False

        try:
            phone_obj = User.objects.get(phone_no = phone_no)
            phone = True

        except:
            phone = False

            #Checks if user with the same email and phone exists

        if phone:
            raise serializers.ValidationError(f'{phone_obj.user_type} with this phone already exists')
       
        if user:
            raise serializers.ValidationError(f'{email_obj.user_type} with this email already exists')
       
        user_obj = User.objects.create(email=email,phone_no=phone_no,user_type = 'passenger')
    
        user_obj.first_name = validated_data.pop('first_name',None)
        user_obj.last_name = validated_data.pop('last_name',None)
        user_obj.user_picture = validated_data.pop('user_picture',None)
        user_obj.set_password(validated_data.pop('password',None))
        user_obj.save()

        # passenger_obj.save()
        # try:

        passenger_obj = passenger.objects.create(user = user_obj )
        # except:
        #     raise serializers.ValidationError('Passenger with this email AND phone already exists')

        return passenger_obj
        
class RiderSerializer(serializers.ModelSerializer):

    

    email = serializers.EmailField(write_only=True, required=True)
    car_pic = serializers.ImageField(write_only=True, required=True)
    license = serializers.FileField(write_only = True)
    type = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(write_only=True, required=True)
    last_name =  serializers.CharField(write_only=True, required=True)
    seat_cap = serializers.IntegerField(write_only=True, required=True)
    brand = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    plate_no = serializers.CharField(write_only=True, required=True)
    phone_no = serializers.CharField(write_only=True, required=True)
    user_picture = serializers.ImageField(write_only=True, required=True)
    trip_duration = serializers.CharField(write_only=True, required=True)

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
                  'type',
                  'car_pic',
                  'seat_cap',
                  'brand',
                  'password',
                  'plate_no',
                  'email',
                  'phone_no',
                  'trip_duration',
                  'user_picture',
                  

                  ]
     

    def create (self,validated_data):
        
        email = validated_data.get('email',None)
        phone_no = validated_data.get('phone_no',None)
       
        plate_no = validated_data.get('plate_no',None)

        try:
            email_obj = User.objects.get(email = email)
            user = True
        
        except:
            user = False

        try:
            phone_obj = User.objects.get(phone_no = phone_no)
            phone = True

        except:
            phone = False

            #Checks if user with the same email and phone exists

        if phone:
            raise serializers.ValidationError(f'{phone_obj.user_type} with this  phone already exists')
       
        if user:
            raise serializers.ValidationError(f'{email_obj.user_type} with this email already exists')
            


        #checks if a car with the plate number has already been registered

        try:
            vehicle.objects.get(plate_no = plate_no)
            plate_no = True
        
        except:
            plate_no = False
            
        
        if plate_no:
            raise serializers.ValidationError('Vehicle with this plate_no already exists')
        
        
   
     
        
        user_obj = User.objects.create(
            email = email, 
            phone_no = phone_no,
            user_type = 'rider'
            )
        
        
        # print(validated_data)
        # print(user_obj)
        
        user_obj.first_name = validated_data.get('first_name',None)
        user_obj.last_name = validated_data.get('last_name',None)
        user_obj.user_picture = validated_data.get('user_picture',None)
        user_obj.phone_no = validated_data.get('phone_no',None)
        user_obj.set_password(validated_data.get('password',None))
       
        user_obj.save()

     

        
        # print('user_id',user_obj)

        vehicle_obj = vehicle.objects.create(
                picture = validated_data.get('car_pic',None),
                type = validated_data.get('type',None),
                brand = validated_data.get('brand',None),
                plate_no = validated_data.get('plate_no',None),
                seat_cap = validated_data.get('seat_cap', None ),
                # seat_available = validated_data.get('seat_cap', None ),

        )
        # vehicle_obj.save()

        
        rider_obj = rider.objects.create(
            user = user_obj,
            vehicle = vehicle_obj,
            route_from = validated_data.get('route_from',None),
            route_to = validated_data.get('route_to',None),
            bus_stop = validated_data.get('bus_stop',None),
            licence = validated_data.get('license',None),
            price = validated_data.get('price',None),
            trip_duration = validated_data.get('trip_duration', None),

            )
        # rider_obj.save()
        
        
        
        

        return rider_obj

   