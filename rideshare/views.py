import json
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView,UpdateAPIView,GenericAPIView
from .permissions import IsVerifiedAndPassanger,IsVerifiedAndRider
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.parsers import (JSONParser,
                                    MultiPartParser, 
                                    FormParser, FileUploadParser)
from rest_framework import mixins
from django.shortcuts import get_object_or_404

from .models import rider,passenger,Order,Trip,vehicle
from .serializers import (RiderSerializer,
                          OrderSerializer,
                          TripSerializer,PassengerSerializer,
                          AccountDetailSerializer,
                          VehicleSerializer)
from .permissions import IsVerifiedAndPassanger,IsVerifiedAndRider
from.utils import initialize_trans,verify
User = get_user_model()


class PayForRide(APIView):
    permission_classes= [IsAuthenticated&IsVerifiedAndPassanger]
    def post(self,request, *args, **kwargs):
        order = Order.objects.get(id=request.data.get('order_id'))
        # print(int(order.rider.price)*100,'price')
        data = {
            'email': order.passenger.user.email,
           
            'amount': (int(order.rider.price) * 100),
            # 'order_id':request.data.get('order_id')
        }
        trans_data = initialize_trans(data)
        order.reference = trans_data.get('data').get('reference')
        order.save()

        return Response(trans_data)

class SearchForRide(APIView):
    permission_classes= [IsAuthenticated&IsVerifiedAndPassanger]
    parser_classes = ( MultiPartParser, FormParser,JSONParser,FileUploadParser)

    def post(self, request, *arg, **kwarg):
        # print("request data",request.data)
        route_to = request.data.get('route_to')
        # route_from =  request.data.route_from 
        min_price = request.data.get('min_price')
        max_price = request.data.get('max_price')
        vehicle_count_gte_one = [vehicle.id for vehicle in vehicle.objects.all() if int(vehicle.seat_available)>=1]
        rides = rider.objects.filter(vehicle__in=vehicle_count_gte_one,is_active=True,route_to=route_to, price__lte = max_price, price__gte=min_price )

        serializer = RiderSerializer(rides,many=True)
        # print(rides_list,"ride list")
        # if serializer.is_valid(raise_exception=True):
            # print(serializer.data,"ride list")
        return Response({'Rides':serializer.data})
        
class GoOnline(APIView):
    permission_classes= [IsAuthenticated&IsVerifiedAndRider]

    def get(self, request, *arg, **kwarg):
        user = request.user
        _rider = rider.objects.get(user = user)
        if _rider.is_active == True:
            return Response({"message":"User already online"})
        
        _rider.is_active = True
        _rider.save()
        return Response({"message":"User is now active and can recive orders"})

class GoOffline(APIView):
    permission_classes= [IsAuthenticated&IsVerifiedAndRider]
    
    def get(self, request, *arg, **kwarg):
        user = request.user
        _rider = rider.objects.get(user = user)
        if _rider.is_active == False:
            return Response({"message":"User already offline"})
        
        _rider.is_active = False
        _rider.save()
        return Response({"message":"User is now offline and will not recive orders"})
    
class CreateOrder(CreateAPIView, mixins.UpdateModelMixin):
    """
    receive a post request with driver id, creates and return an order
    """
    permission_classes= [IsAuthenticated&IsVerifiedAndPassanger]
    serializer_class = [OrderSerializer]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # print(request.data,"data")
        # passenger_ride = passenger.objects.get(user = request.user)

        # driver_user = User.objects.get(rider = request.data.get('rider_id'))
        # driver = rider.objects.get(user = driver_user)
        
    
        passenger_obj =passenger.objects.get(user = request.user.id)
        # print(request.user.id,"data")
        rider_new= get_object_or_404(rider,id=request.data.get('rider_id'))
        passenger_new = get_object_or_404(passenger, id = passenger_obj.id)

        data = {
            "passenger": passenger_new.id,
            # "rider": request.data.get('rider_id')
        }
        
  
        serializer = OrderSerializer(data = data)
        serializer.is_valid(raise_exception=True)
        serializer.save(rider=rider_new,passenger=passenger_new)
        
        # order_obj =self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # driver.vehicle.seat_available -= 1
        # driver.vehicle.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def partial_update(self, request, *args, **kwargs):
        order = Order.objects.get(id = request.data.get('order_id'))
        order.passenger_order_status = request.data.get('status')
        order.save()
        serailized_order = OrderSerializer(order)
        return Response(serailized_order.data)
    
class VerifyPay(APIView):
    def get (self,request,*args,**kwargs):
        ref = request.GET.get('reference')
        verify_res = verify(ref)
        order_obj = Order.objects.get(reference = verify_res.get('data').get('reference'))

        if verify_res.get('data').get('status') == 'success' and int(order_obj.rider.price)*100 == verify_res.get('data').get('amount'):
            # order_obj.rider.vehicle.seat_available-=1
            # order_obj.rider.vehicle.save()
            order_obj.has_paid = True
            order_obj.save()

            return Response({"message":"transaction sucessful"})
        
            
        else:

            return Response({"error":"transaction failed"})

class ListCusOrder(ListAPIView):
    permission_classes= [IsAuthenticated&IsVerifiedAndPassanger]
    serializer_class=[OrderSerializer]



    def list(self, request, *args, **kwargs):
            passenger_obj = passenger.objects.get(user = request.user)

            query = Order.objects.filter(passenger = passenger_obj,has_paid = True)
            serializer = OrderSerializer(query, many=True)
            return Response(serializer.data)
    
    # def get_queryset(self,user):
    #     passenger_obj = passenger.objects.get(user = user)
    #     queryset = Order.objects.filter(passenger = passenger_obj,has_paid = True)

class ListRiderOrder(ListAPIView):
    permission_classes= [IsAuthenticated&IsVerifiedAndRider]
    serializer_class=[OrderSerializer]

    def list(self, request, *args, **kwargs):
            rider_obj = rider.objects.get(user = request.user)

            query = Order.objects.filter(rider = rider_obj,has_paid = True,rider_order_status=None)
            serializer = OrderSerializer(query, many=True)
            # print(serializer)
            
            return Response(serializer.data)
    
"list orders that our the driver and the rider status is blank"

class AcceptOrder(APIView):
    permission_classes= [IsAuthenticated&IsVerifiedAndRider]
    def get(self,request,*arg,**kwarg):

        order_id = request.GET.get('order_id')
        rider_obj = rider.objects.get(user = request.user)
        order_obj = Order.objects.get(id = order_id)
        passsenger_count_lt_seat_cap = [trip.id for trip in Trip.objects.all() if int(trip.passenger_count)<rider_obj.vehicle.seat_cap]
        trip_obj = Trip.objects.filter(rider = rider_obj,id__in = passsenger_count_lt_seat_cap).exclude(rider_order_status='Completed').exclude(rider_order_status ='Cancelled')[0]
        if not trip_obj:
            trip_obj = Trip.objects.create(rider=rider_obj,rider_order_status = 'Accepted')
        order_obj.trip = trip_obj
        # trip_obj.passenger_count+=1
        order_obj.rider_order_status='Accepted'
        trip_obj.save()
        order_obj.save()
        serialized_trip = TripSerializer(trip_obj)

        return Response(serialized_trip.data)
        
    "get or create trip with this rider and has status accepted"
    
class ViewATrip(APIView):
    permission_classes= [IsAuthenticated&IsVerifiedAndRider]
    def get(self,request,*arg,**kwargs):
        trip = get_object_or_404(Trip, id = request.GET.get('id'))
        serialized_trip = TripSerializer(trip)
        return Response(serialized_trip.data)

    # serializer_class = TripSerializer
    # queryset= Trip.objects.all()
    # lookup_field = ['id']



class DeclineOrder(APIView):
    permission_classes= [IsAuthenticated&IsVerifiedAndRider]
    
    def get(self,request,*arg,**kwarg):
        order_obj = get_object_or_404(Order,id = request.GET.get('id'))
        # order_obj.rider.vehicle.seat_available+=1
        trip_obj = Trip.objects.get_or_create(rider= order_obj.rider,rider_order_status = 'Accepted')[0]
        # trip_obj.passenger_count-=1
        order_obj.rider.vehicle.save()
        order_obj.rider_order_status = "Declined"
        order_obj.passenger_order_status = "Cancelled"
        order_obj.save()
        trip_obj.save()

        serialized_trip = TripSerializer(trip_obj)

        return Response(serialized_trip.data)


class EditDriverProfile(UpdateAPIView):
    permission_classes= [IsAuthenticated&IsVerifiedAndRider]
    serializer_class = RiderSerializer
    lookup_field='pk'


class EditRoute(UpdateAPIView):
    permission_classes= [IsAuthenticated&IsVerifiedAndRider]
    serializer_class = RiderSerializer
    lookup_field='pk'

class GetVehicleDetail(APIView):
   permission_classes= [IsAuthenticated&IsVerifiedAndRider]
   def get(self,request,*arg,**kwargs):
        vehicle_obj = get_object_or_404(vehicle, id = request.GET.get('id'))
        serialized_vehicle = VehicleSerializer(vehicle_obj)
        return Response(serialized_vehicle.data)

class UpdateTripStatus(APIView,mixins.UpdateModelMixin):
    permission_classes= [IsAuthenticated&IsVerifiedAndRider]
    def partial_update(self, request, *args, **kwargs):
        trip_obj = Trip.objects.get(id = request.data.get('trip_id'))
        status = request.data.get('status')
        trip_obj.rider_order_status = status
        trip_obj.save()

        orders = Order.objects.filter(trip=trip_obj)
        for order in orders:
            order.status = status
            order.save()
            # if status == 'completed' and order.passenger_order_status == 'completed':
            #     send_driver_money()
            

       
        serailized_trip = TripSerializer(trip_obj)
        return Response(serailized_trip.data)
    
class UpdateorderStatus(GenericAPIView,mixins.UpdateModelMixin):
    permission_classes= [IsAuthenticated&IsVerifiedAndRider]

    def partial_update(self, request, *args, **kwargs):

        status = request.data.get('status')
        order_ = Order.objects.get(id=request.data.get('order_id'))
        trip_ = Trip.objects.get(id = order_.trip)

        # if status == 'completed' and trip_.rider_status == 'completed':
        #     send_driver_money()
            
        order_.status = status
        order_.save()

       
        serailized_trip = OrderSerializer(order_)
        return Response(serailized_trip.data)
    
class CreateUpdateBankAccount(CreateAPIView):
    permission_classes = [IsAuthenticated&IsVerifiedAndRider]
    serializer_class = AccountDetailSerializer
    
class Webhook(APIView): #webhook for receiving and sending payment

    def post(self,request,*arg,**kwarg):
        order_obj = Order.objects.get(reference = request.data.get('data').get('reference'))
        if request.data.get('event') == 'charge.success' and int(order_obj.landmark.price)*100 == request.data.get('data').get('amount'):
            order_obj.trip.rider.vehicle.seat_available-=1
            order_obj.trip.rider.vehicle.save()
            order_obj.has_paid = True
            order_obj.rider_pay_ref = uuid.uuid4()
            order_obj.order_datetime = datetime.datetime.now()
            order_obj.save()
        elif request.data.get('event') == 'transfer.failed':
            data = {
                    "amount": order_obj.rider_pay,
                    "reference": order_obj.rider_pay_ref,
                    "recipient": order_obj.rider.account.recipient_code
                }
            make_transfer(data)
        return Response(status=status.HTTP_200_OK)
