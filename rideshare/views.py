import json
import datetime
import uuid
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    DestroyAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from .permissions import IsVerifiedAndPassanger, IsVerifiedAndRider, IsVerified
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework import mixins
from django.shortcuts import get_object_or_404

from .models import Rider, Order, Trip, Vehicle, RiderLandmark
from .serializers import (
    RiderSerializer,
    OrderSerializer,
    CreateOrderSerializer,
    RiderLandmarkSerializer,
    UserSerializer,
    ListRiderOrderSerializer,
    TripSerializer,
    AccountDetailSerializer,
    VehicleSerializer,
)
from .permissions import IsVerifiedAndPassanger, IsVerifiedAndRider
from .utils import (
    initialize_trans,
    make_transfer,
    riders_working_now,
    create_recipient,
    verify_account_no,
    riders_working_today,
)


User = get_user_model()


class PayForRide(APIView):
    permission_classes = [IsAuthenticated & IsVerifiedAndPassanger]

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(id=request.data.get("order_id"))
        if request.user == order.passenger:
            data = {
                "email": order.passenger.email,
                "amount": (int(order.landmark.price) * 100),
            }

            trans_data = initialize_trans(data)
            order.reference = trans_data.get("data").get("reference")
            order.save()
            return Response(trans_data)

        return Response(
            {"message": "auth user did not create this order hence cannot pay for it"}
        )


class SearchForRide(APIView):
    permission_classes = [IsAuthenticated & IsVerifiedAndPassanger]

    def post(self, request, *arg, **kwarg):
        current_datetime = datetime.datetime.now()
        current_day_no = int(current_datetime.strftime("%w"))
        current_time = current_datetime.time()

        route_to = request.data.get("route_to")

        min_price = request.data.get("min_price")
        max_price = request.data.get("max_price")
        vehicle_count_gte_one = [
            vehicle.id
            for vehicle in Vehicle.objects.all()
            if int(vehicle.seat_available) >= 1
        ]

        riders_first_filter = Rider.objects.filter(
            vehicle__in=vehicle_count_gte_one, is_active=True, route_to=route_to
        )

        riders_second_filter = [
            rider
            for rider in riders_first_filter
            if rider.price <= int(max_price) and rider.price >= int(min_price)
        ]
        print(riders_second_filter)
        riders_working_day = riders_working_today(riders_second_filter, current_day_no)
        print(riders_working_day)

        riders_working_time = riders_working_now(riders_working_day, current_time)
        trips = Trip.objects.filter(rider__in=riders_working_time)
        serializer = TripSerializer(trips, many=True)
        return Response({"Trips": serializer.data})


class GoOnline(APIView):
    permission_classes = [IsAuthenticated & IsVerifiedAndRider]

    def get(self, request, *arg, **kwarg):
        user = request.user
        _rider = Rider.objects.get(user=user)
        Trip.objects.create(rider=_rider, rider_order_status="")

        if _rider.is_active == True:
            return Response({"message": "User already online"})

        _rider.is_active = True
        _rider.save()
        return Response({"message": "User is now active and can recive orders"})


class GoOffline(APIView):
    permission_classes = [IsAuthenticated & IsVerifiedAndRider]

    def get(self, request, *arg, **kwarg):
        user = request.user
        _rider = Rider.objects.get(user=user)

        try:
            # delete trip with no order , new trip is created when the rider is online
            Trip.objects.get(rider=_rider, rider_order_status="").delete()

            # periodically delete orders created by users who did not pay, since there isnt a better place the periodic delete, orders that are not paid for on trips that has been completed attach to riders are deleted when they(riders) go offline
            trip = Trip.objects.get(rider=_rider.id, completed=True)
            for order in Order.objects.filter(has_paid=False, trip=trip):
                order.delete()
        except:
            pass

        if _rider.is_active == False:
            return Response({"message": "User already offline"})

        _rider.is_active = False
        _rider.save()
        return Response({"message": "User is now offline and will not recive orders"})


class ListCusOrder(ListAPIView):
    permission_classes = [IsAuthenticated & IsVerifiedAndPassanger]
    serializer_class = [OrderSerializer]

    def list(self, request, *args, **kwargs):
        passenger_obj = User.objects.get(id=request.user.id)

        query = Order.objects.filter(
            passenger=passenger_obj,has_paid = True
        )  
        serializer = OrderSerializer(query, many=True)
        return Response(serializer.data)


class UpdateOrderStatus(UpdateAPIView):
    permission_classes = [IsAuthenticated & IsVerifiedAndPassanger]

    def partial_update(self, request, *args, **kwargs):
        status = request.data.get("status")
        order_ = get_object_or_404(Order, id=request.data.get("order_id"))

        # if status == 'completed' and trip_.rider_status == 'completed':
        #     send_driver_money()

        order_.passenger_order_status = status
        order_.save()

        serailized_trip = OrderSerializer(order_)
        return Response(serailized_trip.data)


class CreateOrder(CreateAPIView, mixins.UpdateModelMixin):
    """
    receive a post request with driver id, creates and return an order
    """

    permission_classes = [IsAuthenticated & IsVerifiedAndPassanger]

    def create(self, request, *args, **kwargs):
        trip_new = get_object_or_404(Trip, id=request.data.get("trip_id"))
        passenger_new = get_object_or_404(User, id=request.user.id)
        orders_count = Order.objects.filter(
            passenger=passenger_new, trip=trip_new
        ).count()
        if not orders_count == 0:
            return Response({"message": "you are already registered on this trip"})
        data_ = {
            "passenger": passenger_new.id,
            "trip": request.data.get("trip_id"),
            "landmark": request.data.get("landmark_id")
        }


        serializer = CreateOrderSerializer(data=data_)
        serializer.is_valid(raise_exception=True)

        order_obj = serializer.save()
        headers = self.get_success_headers(serializer.data)

        serializer2 = OrderSerializer(order_obj)

        return Response(
            serializer2.data, status=status.HTTP_201_CREATED, headers=headers
        )

class YesConfirmedStatus(UpdateAPIView):
    """
    a notification is sent to passengers asking them to confirm if they'r e in transit
    """

    permission_classes = [IsAuthenticated & IsVerifiedAndPassanger]
    serializer_class = [OrderSerializer]

    def partial_update(self, request, *args, **kwargs):
        trip_ = Trip.objects.filter(id=request.data.get("trip_id"))
        order_ = Order.objects.filter(trip__in=trip_, passenger=request.user.id).first()
        order_.passenger_order_status = "On Transit"
        order_.save()
        serailized_trip = OrderSerializer(order_)
        return Response(serailized_trip.data)


class ViewAOrder(RetrieveAPIView):
    permission_classes = [IsAuthenticated & IsVerifiedAndPassanger]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    lookup_field = "trip_id"


class ListRiderOrder(ListAPIView):
    permission_classes = [IsAuthenticated & IsVerifiedAndRider]

    def list(self, request, *args, **kwargs):
        rider_obj = Rider.objects.get(user=request.user)
        query = Order.objects.filter(trip__rider=rider_obj, rider_order_status=None)
        serializer = ListRiderOrderSerializer(query, many=True)
        return Response(serializer.data)


class AcceptOrder(APIView):
    permission_classes = [IsAuthenticated & IsVerifiedAndRider]

    def get(self, request, *arg, **kwarg):
        order_id = request.GET.get("order_id")
        order_obj = Order.objects.get(id=order_id)
        order_obj.rider_order_status = "Accepted"
        order_obj.save()
        return Response(
            {"message": f"order accepted, prompt user to pay", "order_id": order_id}
        )


class ViewATrip(APIView):
    permission_classes = [IsAuthenticated & IsVerifiedAndRider]

    def get(self, request, *arg, **kwargs):
        trip = get_object_or_404(Trip, id=request.GET.get("trip_id"))
        serialized_trip = TripSerializer(trip)
        return Response(serialized_trip.data)


class ViewCompletedTrips(ListAPIView):
    permission_classes = [IsAuthenticated & IsVerifiedAndRider]
    serializer_class = TripSerializer

    def list(self, request, *args, **kwargs):
        get_rider = Rider.objects.get(user=request.user.id)
        queryset = Trip.objects.filter(rider=get_rider, rider_order_status="Completed")
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ViewOngoingTrips(ListAPIView):
    permission_classes = [IsAuthenticated & IsVerifiedAndRider]
    serializer_class = TripSerializer

    def get_queryset(self):
        return super().get_queryset()

    def list(self, request, *args, **kwargs):
        get_rider = Rider.objects.get(user=request.user.id)
        queryset = Trip.objects.filter(rider=get_rider).exclude(
            rider_order_status="Completed"
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class DeclineOrder(APIView):
    permission_classes = [IsAuthenticated & IsVerifiedAndRider]

    def get(self, request, *arg, **kwarg):
        order_obj = get_object_or_404(Order, id=request.GET.get("order_id"))
        order_obj.delete()

        return Response({"message": "order declined send notification to user "})


class EditUserProfile(UpdateAPIView):
    permission_classes = [IsAuthenticated & IsVerified]
    serializer_class = UserSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        return serializer.save()

    def update(self, request, *args, **kwargs):
        instance = User.objects.get(id=request.user.id)
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        obj = self.perform_update(serializer)
        obj.is_verified = True
        password = request.data.get("password")

        if password:
            obj.set_password(password)

        obj.save()
        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class EditRoute(UpdateAPIView):
    permission_classes = [IsAuthenticated & IsVerifiedAndRider]
    serializer_class = RiderSerializer
    lookup_field = "pk"


class GetVehicleDetail(APIView):
    permission_classes = [IsAuthenticated & IsVerifiedAndRider]

    def get(self, request, *arg, **kwargs):
        rider = Rider.objects.get(user=request.user)
        vehicle = Vehicle.objects.get(rider=rider.id)
        vehicle_obj = get_object_or_404(Vehicle, id=vehicle.id)
        serialized_vehicle = VehicleSerializer(vehicle_obj)
        return Response(serialized_vehicle.data)


class GetUserProfile(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = User.objects.get(id=request.user.id)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UpdateTripStatus(UpdateAPIView):
    permission_classes = [IsAuthenticated & IsVerifiedAndRider]

    def partial_update(self, request, *args, **kwargs):
        trip_obj = Trip.objects.get(id=request.data.get("trip_id"))
        status = request.data.get("status")
        trip_obj.rider_order_status = status
        trip_obj.save()

        orders = Order.objects.filter(trip=trip_obj)
        for order in orders:
            order.rider_order_status = status
            order.save()
            if status == "Pick up":
                order.order_datetime = datetime.datetime.now()
                trip_obj.started_at = datetime.datetime.now()
            if status == "Completed" and order.passenger_order_status == "Completed":
                data = {
                    "amount": order.rider_pay,
                    "reference": order.rider_pay_ref,
                    "recipient": order.rider.account.recipient_code,
                }
                make_transfer(data)

        serailized_trip = TripSerializer(trip_obj)
        return Response(serailized_trip.data)


class CreateUpdateBankAccount(CreateAPIView):
    permission_classes = [IsAuthenticated & IsVerifiedAndRider]

    def create(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        rider = Rider.objects.get(user=user)
        data = {
            "bank_code": request.data.get("bank_code"),
            "account_number": request.data.get("account_number"),
        }


        acnt_no = verify_account_no(data)

        if acnt_no.get("status") == True:
            data2 = {
                "account_number": acnt_no.get("data").get("account_number"),
                "account_name": acnt_no.get("data").get("account_name"),
                "bank_code": request.data.get("bank_code"),
            }
            recipient = create_recipient(data2)

            data3 = {
                "account_number": recipient.get("data")
                .get("details")
                .get("account_number"),
                "bank_code": recipient.get("data").get("details").get("bank_code"),
                "account_name": recipient.get("data")
                .get("details")
                .get("account_name"),
                "recipient_code": recipient.get("data").get("recipient_code"),
            }
            serializer = AccountDetailSerializer(data=data3)
            serializer.is_valid(raise_exception=True)
            acnt_obj = serializer.save(rider_id=rider.id)
            rider.account = acnt_obj
            rider.save()

            return Response(serializer.data)
        return Response(acnt_no)


class ListAddLandmark(CreateAPIView, ListAPIView, DestroyAPIView):
    serializer_class = RiderLandmarkSerializer
    permission_classes = [IsAuthenticated & IsVerifiedAndRider]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        landmark_list = request.data.get("landmarks")
        get_rider = Rider.objects.get(user=request.user.id)
        for data in landmark_list:
            data = {**data, "rider": get_rider.id}
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

        query = RiderLandmark.objects.filter(rider=get_rider)

        return Response(
            RiderLandmarkSerializer(query, many=True).data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def list(self, request, *args, **kwargs):
        get_rider = Rider.objects.get(user=request.user.id)
        queryset = RiderLandmark.objects.filter(rider=get_rider)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class DeleteLandmark(DestroyAPIView):
    serializer_class = RiderLandmarkSerializer
    permission_classes = [IsAuthenticated & IsVerifiedAndRider]
    queryset = RiderLandmark.objects.all()
    lookup_field = "id"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        get_rider = Rider.objects.get(user=request.user.id)

        get_landmarks = RiderLandmark.objects.filter(rider=get_rider.id)
        serializer = self.get_serializer(get_landmarks, many=True)
        return Response(serializer.data)


class GetRiderDetail(RetrieveAPIView):
    serializer_class = RiderSerializer
    permission_classes = [IsAuthenticated & IsVerifiedAndPassanger]
    queryset = Rider.objects.all()
    lookup_field = 'id'


class Webhook(APIView):  # webhook for receiving and sending payment
    def post(self, request, *arg, **kwarg):
        order_obj = Order.objects.get(
            reference=request.data.get("data").get("reference")
        )

        if request.data.get("event") == "charge.success" and int(
            order_obj.landmark.price
        ) * 100 == request.data.get("data").get("amount"):

            order_obj.trip.rider.vehicle.save()
            order_obj.has_paid = True
            order_obj.rider_pay_ref = uuid.uuid4()
            order_obj.order_datetime = datetime.datetime.now()
            order_obj.save()

        elif request.data.get("event") == "transfer.failed":
            data = {
                "amount": order_obj.rider_pay,
                "reference": order_obj.rider_pay_ref,
                "recipient": order_obj.rider.account.recipient_code,
            }

            make_transfer(data)
        return Response(status=status.HTTP_200_OK)
