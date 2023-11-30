import datetime
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


def upload_data(instance, filename):
    return f"to_go/{instance.user.first_name}_{instance.user.last_name}_{instance.user.id}/document/{filename}"


def upload_vehicle_pic(instance, filename):
    return f"to_go/plate_no/{instance.plate_no}/document/{filename}"


class Vehicle(models.Model):
    choices = [
        ("Car", "Car"),
        ("Bus", "Bus"),
        ("Tricycle", "Tricycle"),
        ("Motocycle", "Motorcycle"),
    ]
    picture = models.ImageField(upload_to=upload_vehicle_pic, null=True, blank=True)
    type = models.CharField(choices=choices, max_length=10)
    brand = models.CharField(max_length=125)
    plate_no = models.CharField(max_length=125)
    seat_cap = models.IntegerField()

    @property
    def seat_available(self):
        rider_ = Rider.objects.get(vehicle=self)

        # if rider has no trip started, vehicle still has full capacity
        try:
            trip = Trip.objects.get(rider=rider_)
            pending_orders = (
                Order.objects.filter(trip=trip, has_paid=True)
                .exclude(rider_order_status="Completed")
                .count()
            )
            return int(self.seat_cap) - int(pending_orders)
        except:
            return int(self.seat_cap)


class AccountDetail(models.Model):
    account_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=125)
    bank_code = models.CharField(max_length=4)
    recipient_code = models.CharField(max_length=50)


class Rider(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="rider"
    )
    vehicle = models.OneToOneField(
        Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name="rider"
    )
    account = models.OneToOneField(
        AccountDetail,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rider",
    )
    route_from = models.CharField(max_length=125)
    route_to = models.CharField(max_length=125)
    trip_duration = models.CharField(max_length=10)
    bus_stop = models.CharField(max_length=125)
    licence = models.FileField(upload_to=upload_data, null=True, blank=True)
    rider_price = models.IntegerField()
    is_active = models.BooleanField(default=False)
    schedule = models.JSONField()

    @property
    def today_trips(self):
        my_trips = Trip.objects.filter(rider=self)
        todays_date = datetime.datetime.now().date()
        today_trips = [trip for trip in my_trips if trip.get_date == todays_date]
        return today_trips

    @property
    def service_charge(self):
        if 200 <= int(self.rider_price) <= 800:
            return 80
        if 900 <= int(self.rider_price) <= 2500:
            return 90
        if int(self.rider_price) <= 2600:
            return 100

    @property
    def today_trips_no(self):
        return len(self.today_trips)

    @property
    def today_earnings(self):
        trips_today = self.today_trips
        total = 0
        for i in trips_today:
            total += i.amount_raised
        return total

    @property
    def price(self):
        return self.rider_price + self.service_charge


class Trip(models.Model):
    rider_status = [
        ("Pick Up", "Pick Up"),
        ("On Transit", "On Transit"),
        ("Completed", "Completed"),
    ]

    amount_raised = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    rider_order_status = models.CharField(
        choices=rider_status, null=True, blank=True, max_length=10
    )
    started_at = models.DateTimeField(auto_now_add=True)

    @property
    def passenger_count(self):
        return Order.objects.filter(trip=self.id).count()

    @property
    def formated_createdAt(self):
        created_datetime = self.started_at
        formatted = created_datetime.strftime("%a, %d %B, %Y")
        return formatted

    @property
    def get_date(self):
        created_datetime = self.started_at
        today_date = created_datetime.date()
        return today_date

    @property
    def get_end_time(self):
        trip_duration_split = self.rider.trip_duration.split()  # ['1hr,20min]
        hr_duration = int(trip_duration_split[0][0])
        min_duration = int(trip_duration_split[1][:2])
        created_datetime = self.started_at
        end_time = created_datetime + datetime.timedelta(
            hours=hr_duration, minutes=min_duration
        )
        return end_time.strftime("%I:%M %p")

    @property
    def get_started_time(self):
        created_datetime = self.started_at
        start_time = created_datetime.strftime("%I:%M %p")
        return start_time


class RiderLandmark(models.Model):
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE, related_name="landmark")
    route_to = models.CharField(max_length=255)
    rider_price = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def service_charge(self):
        if 200 <= int(self.rider_price) <= 800:
            return 80
        if 900 <= int(self.rider_price) <= 2500:
            return 90
        if int(self.rider_price) <= 2600:
            return 100

    @property
    def price(self):
        return self.rider_price + self.service_charge


class Order(models.Model):
    rider_order_status = [
        ("Accepted", "Accepted"),
        ("Pick Up", "Pick Up"),
        ("On Transit", "On Transit"),
        ("Completed", "Completed"),
    ]

    passenger_order_status = [
        ("Pending", "Pending"),
        ("On Transit", "On Transit"),
        ("Completed", "Completed"),
    ]
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="trip")
    # rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    landmark = models.ForeignKey(
        RiderLandmark, on_delete=models.SET_NULL, null=True, blank=True
    )
    passenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    reference = models.CharField(max_length=20, blank=True, null=True)
    order_datetime = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    has_paid = models.BooleanField(default=False)
    rider_pay_ref = models.UUIDField(null=True, blank=True)
    passenger_order_status = models.CharField(
        choices=passenger_order_status, default="Pending", max_length=10
    )
    rider_order_status = models.CharField(
        choices=rider_order_status, max_length=10, null=True, blank=True
    )

    @property
    def rider_pay(self):
        pay = int(self.landmark.price) * 0.9
        return pay
