from django.contrib import admin
from .models import Passenger, Booking,Payment



# Register your models here.
admin.site.register(Passenger)
admin.site.register(Booking)
admin.site.register(Payment)
