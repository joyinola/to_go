from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from .models import passenger

"""
rider reg -- creates, user, vehicle, rider, sends otp 
"""
User = get_user_model()
class PassangerSerialzier(serializers.ModelSerializer):
    password =  serializers.SerializerMethodField(write_only = True, required = False)
    
    
    class Meta:
        model = User
        fields = [
            'email',
            'password',
            
        ]

        def create (self,validated_data):
            try:
                user_obj = User.objects.create(
                email = validated_data.pop('email',None))

            except IntegrityError:
                raise serializers.ValidationError('User already exists')


            user_obj.first_name = validated_data.pop('first_name',None),
            user_obj.last_name = validated_data.pop('last_name',None)
            user_obj.set_password(validated_data.pop('password',None))
            user_obj.save()

            passenger_obj = passenger.objects.create(user=user_obj)
            passenger_obj.save()


            

            return passenger_obj
            
        




