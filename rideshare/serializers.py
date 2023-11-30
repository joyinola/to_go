import datetime
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Rider, Vehicle, Order, Trip, AccountDetail, RiderLandmark

User = get_user_model()


class RequestPassswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "id",
            "last_name",
            "email",
            "phone_no",
            "is_verified",
            "user_picture",
        ]


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ["seat_available", "picture", "type", "brand", "plate_no", "seat_cap"]


class RiderLandmarkSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = RiderLandmark
        fields = ["id", "rider", "route_to", "rider_price", "price"]

    def get_price(self, obj):
        return int(obj.rider_price) + obj.service_charge


class RiderSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer()
    user = UserSerializer()
    landmark = serializers.SerializerMethodField()
    total_trips = serializers.SerializerMethodField()

    class Meta:
        model = Rider
        fields = [
            "id",
            "landmark",
            "user",
            "vehicle",
            "route_from",
            "price",
            "today_earnings",
            "today_trips_no",
            "total_trips",
        ]

    def get_total_trips(self, obj):
        return Trip.objects.filter(rider=obj).count()

    def get_landmark(self, obj):
        landmarks = RiderLandmark.objects.filter(rider=obj)
        return RiderLandmarkSerializer(landmarks, many=True).data


class RiderLandmarkSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = RiderLandmark
        fields = ["id", "rider", "route_to", "rider_price", "price"]

    def get_price(self, obj):
        return int(obj.rider_price) + obj.service_charge


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "passenger",
            "trip",
            "passenger_order_status",
            "landmark",
            "has_paid",
        ]

    def create(self, validated_data):
        print(validated_data)
        trip = validated_data.pop("trip")
        order_obj = Order.objects.create(
            #    rider = trip.rider,
            trip=trip,
            passenger=validated_data.pop("passenger"),
            landmark=validated_data.pop("landmark"),
            passenger_order_status="pending",
        )
        return order_obj


class OrderSerializer(serializers.ModelSerializer):
    passenger = UserSerializer()
    landmark = RiderLandmarkSerializer()
    other_passengers = serializers.SerializerMethodField()
    passengers_count = serializers.SerializerMethodField()
    estimated_arrival = serializers.SerializerMethodField()
    order_time = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "passenger",
            "trip",
            "other_passengers",
            "estimated_arrival",
            "landmark",
            "order_time",
            "passengers_count",
            "passenger_order_status",
            "has_paid",
        ]

    def create(self, validated_data):
        trip = validated_data.pop("trip")
        order_obj = Order.objects.create(
            trip=trip,
            passenger=validated_data.pop("passenger"),
            landmark=validated_data.pop("landmark"),
            passenger_order_status="pending",
        )
        return order_obj

    def get_other_passengers(self, obj):
        other_orders = Order.objects.filter(trip=obj.trip, has_paid=True).exclude(
            passenger=obj.passenger
        )
        other_passengers = User.objects.filter(orders__in=other_orders)
        others_serialized = UserSerializer(other_passengers, many=True)
        return others_serialized.data

    def get_passengers_count(self, obj):
        other_passenger_count = (
            Order.objects.filter(trip=obj.trip, has_paid=True)
            .exclude(passenger=obj.passenger)
            .count()
        )
        return other_passenger_count

    def get_order_time(self, obj):
        time = str(obj.order_datetime)[11:16]
        time_formatted = datetime.datetime.strptime(time, "%H:%M")
        return time_formatted.strftime("%I:%M %p")

    def get_estimated_arrival(self, obj):
        order_datetime = obj.order_datetime
        trip_duration = obj.trip.rider.trip_duration  # 1hr 20min
        duration_split = trip_duration.split()  # [1hr,20min]
        hour = int(duration_split[0][0])  # 1
        min = int(duration_split[1][:2])  # 20

        end_time = order_datetime + datetime.timedelta(hours=hour, minutes=min)
        return end_time.strftime("%I:%M %p")


class ListRiderOrderSerializer(serializers.ModelSerializer):
    passenger = UserSerializer(read_only=True)
    landmark = RiderLandmarkSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ["id", "passenger", "landmark"]


class TripSerializer(serializers.ModelSerializer):
    rider = RiderSerializer()
    passengers = serializers.SerializerMethodField()
    passenger_count = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = [
            "id",
            "rider",
            "passengers",
            "passenger_count",
            "rider_order_status",
            "formated_createdAt",
            "get_started_time",
            "get_end_time",
        ]

    def get_passengers(self, obj):
        other_orders = Order.objects.filter(trip=obj)
        other_passengers = User.objects.filter(orders__in=other_orders)
        others_serialized = UserSerializer(other_passengers, many=True)
        return others_serialized.data

    def get_passenger_count(self, obj):
        return len(self.get_passengers(obj))


class AccountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountDetail
        fields = "__all__"

    def create(self, validated_data):
        rider_ = Rider.objects.get(id=validated_data.get("rider_id"))
        obj, created = AccountDetail.objects.update_or_create(
            rider=rider_,
            defaults={
                "account_number": validated_data.get("account_number"),
                "bank_code": validated_data.get("bank_code"),
                "account_name": validated_data.get("account_name"),
                "recipient_code": validated_data.get("recipient_code"),
            },
        )
        return obj
