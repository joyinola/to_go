

from datetime import datetime
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import rider,vehicle,Order,passenger,Trip,AccountDetail
User = get_user_model()

class RequestPassswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class UserSerializer(serializers.ModelSerializer):
     class Meta:
          model = User
          fields = ['first_name', 'id','last_name', 'email','is_verified',]

class VehicleSerializer(serializers.ModelSerializer):
     # seat_available = serializers.SerializerMethodField()
     class Meta:
          model = vehicle
          fields = ['seat_available','picture','type', 'brand', 'plate_no', 'seat_cap']

     # def get_seat_available(self,obj):
     #      rider_ = rider.objects.get(vehicle=obj)
     #      pending_orders = Order.objects.filter(rider = rider_, passenger_order_status = 'Accepted').count()
     #      # try:
     #      #      active_trip = Trip.objects.filter(rider = rider_).exclude(rider_order_status='Completed').exclude(rider_order_status ='Cancelled')[0]
     #      # except:
     #      #      return rider_.vehicle.seat_cap
          

     #      return int(rider_.vehicle.seat_cap)-int(pending_orders)

class RiderSerializer(serializers.ModelSerializer):
     vehicle = VehicleSerializer()
     user = UserSerializer()
     class Meta:
          model = rider
          fields = ['id','user','picture','vehicle', 'route_from','route_to','price']

class PassengerSerializer(serializers.ModelSerializer):
     # vehicle = VehicleSerializer()
     user = UserSerializer()
     class Meta:
          model = passenger
          fields = ['id','user','picture']

class OrderSerializer(serializers.ModelSerializer):
     rider = RiderSerializer(read_only=True)
     passenger = PassengerSerializer(read_only = True )
     # rider = serializers.PrimaryKeyRelatedField(many=False, read_only =True)
     # passenger = serializers.PrimaryKeyRelatedField(queryset = passenger.objects.all(), many=False)
     
     other_passengers = serializers.SerializerMethodField()
     passengers_count = serializers.SerializerMethodField()
     estimated_arrival = serializers.SerializerMethodField()
     # order_date = serializers.SerializerMethodField()
     order_time = serializers.SerializerMethodField()
     
     class Meta: 
        model = Order
        fields = ['id','rider','passenger','other_passengers','estimated_arrival' ,'order_time','passengers_count','passenger_order_status', 'has_paid']

     def create(self,validated_data):
        
        rider = validated_data.pop('rider')
        order_obj = Order.objects.create(
             rider = rider,
             passenger = validated_data.pop('passenger'),
             passenger_order_status = "Accepted"
             )
        return order_obj
        
     def get_other_passengers(self, obj):
         other_orders = Order.objects.filter(rider = obj.rider, passenger_order_status = "Accepted" ).exclude(passenger = obj.passenger)
         other_passengers = passenger.objects.filter(orders__in=other_orders)
         others_serialized = PassengerSerializer(other_passengers,many=True)
         return others_serialized.data
     
     def get_passengers_count(self,obj):
          other_passenger_count = Order.objects.filter(rider = obj.rider, passenger_order_status = "Accepted" ).count()
          return other_passenger_count
     
     def get_order_time(self,obj):
          time = str(obj.order_datetime)[11:16]
          time_formatted = datetime.strptime(time,"%H:%M")
          return time_formatted.strftime("%I:%M %p")
     
     
     def get_estimated_arrival(self,obj):
          order_datetime = str(obj.order_datetime)[11:16] #22:10
          trip_duration = obj.rider.trip_duration   #1hr 20min
      
          duration_split = trip_duration.split() #[1hr,20min]
          order_hour = order_datetime[:2] #22   
          order_min = order_datetime[3:] #10
          hour = duration_split[0][0] #1
          min = duration_split[1][:2] #20
          
        
          total_hour = int(order_hour)+int(hour) #22+1
          total_min = int(order_min)
       
        
          if total_hour == 24:
               total_hour=0
        
         
          
          time = f"{total_hour}:{total_min}"

          print(time,'time')

          time_formatted = datetime.strptime(time,"%H:%M")

          return time_formatted.strftime("%I:%M %p")
     
     # def get_order_date(self,obj):
     #      date = str(obj.order_time)[0:10]


class TripSerializer(serializers.ModelSerializer):
#     seat_available = serializers.ModelSerializer()
#     passenger_count = serializers.ModelSerializer()

    rider = RiderSerializer()
    passengers = serializers.SerializerMethodField()

    class Meta:
         model = Trip
         fields = ['id','rider','passengers','order','passenger_count','rider_order_status','created_at']

    def get_passengers(self, obj):
          other_orders = Order.objects.filter(trip = obj, passenger_order_status = "Accepted" )
          other_passengers = passenger.objects.filter(orders__in=other_orders)
          others_serialized = PassengerSerializer(other_passengers,many=True)
          return others_serialized.data
    
#     def get_passenger_count(self,obj):
#          obj_passengers = Order.objects.filter(trip = obj)

#          return obj_passengers.count()
#     def seat_available(self,obj):
#          return int(obj.rider.vehicle.seat_cap)-int(obj.passenger_count)


class AccountDetailSerializer(serializers.ModelSerializer):

     class Meta:
          model = AccountDetail
          fields = '__all__'

     def create(self,validated_data):
          rider_ = rider.objects.get(id = validated_data.get('rider_id'))
          obj,created = AccountDetail.objects.update_or_create(
               rider = rider_, 
               defaults ={
               'account_number': validated_data.get('account_no'),

               }
          )

        

     
