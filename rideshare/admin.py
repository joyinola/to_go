from django.contrib import admin

# Register your models here.
from .models import passenger,rider,vehicle,AccountDetail,Order,Trip

admin.site.register(passenger)
admin.site.register(Trip)
admin.site.register(Order)
admin.site.register(AccountDetail)
admin.site.register(vehicle)
admin.site.register(rider)