from django.contrib import admin

# Register your models here.
from .models import Rider, Vehicle, AccountDetail, Order, Trip, RiderLandmark

# admin.site.register(passenger)
admin.site.register(Trip)
admin.site.register(Order)
admin.site.register(AccountDetail)
admin.site.register(Vehicle)
admin.site.register(Rider)
admin.site.register(RiderLandmark)
