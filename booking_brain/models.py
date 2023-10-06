from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
# from django.core
import random
import string

def generate_unique_code():
    while True:
        code = ''.join(random.choice(string.digits + string.ascii_letters) 
        for _ in range(5))
        if not Booking.objects.filter(Booking_no=code).exists():
            return code


# Create your models here.
    

class Passenger(models.Model):
    id = models.AutoField(primary_key=True)
    Date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    First_name = models.CharField(max_length=50)
    Middle_name = models.CharField(max_length=50)
    Last_name = models.CharField(max_length=50)
    Phone_number = models.CharField(max_length=50)
    Departure_place = models.CharField(max_length=50)
    Destination = models.CharField(max_length=50)
    Departure_date = models.DateField()
    Return_date = models.DateField()
    Amount = models.IntegerField()
    Booked = models.BooleanField(default=False)
    Paid  =  models.BooleanField(default=False)

    

    def __str__(self):
        return (f"{self.First_name} {self.Middle_name} {self.Last_name}")



class Booking(models.Model):
    id =models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Date_created = models.DateTimeField(auto_now_add=True)
    Passport_country = models.CharField(max_length=50) 
    Passport_no = models.CharField(max_length=50)
    Passport_expiry = models.DateField()
    Date_birth = models.DateField()
    Gender = models.CharField(max_length=50)
    # generate random 5 digit 1 alphaber and 4 number
    Booking_no = models.CharField(max_length=5, unique=True, default=generate_unique_code)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)



    def __str__(self):
        return (f'{self.passenger.First_name} {self.passenger.Middle_name} {self.passenger.Last_name} Booking No. is {self.Booking_no} ')

class Payment(models.Model):
    id =models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Date_created = models.DateTimeField(auto_now_add=True)
    Payment_method = models.CharField(max_length=50)
    Payment_status = models.BooleanField(default=True)
    Ticket_no = models.CharField(max_length=50, null=True)
    Payment_ref = models.CharField(max_length=50)
    Amount_EA = models.IntegerField()
    Amount_Z_com = models.IntegerField()
    Amount_M_com = models.IntegerField()
    Amount = models.IntegerField()
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)


    def __str__(self):
        return (f'{self.passenger.First_name} {self.passenger.Middle_name} {self.passenger.Last_name}')


@receiver(post_save, sender=Payment)
def update_payment_in_passengerwhen_created(sender, instance, created, **kwargs):
    if created:
        # When a new payment is created, set ReadyForBooking to True
        instance.passenger.Paid = True
        instance.passenger.save()

@receiver(post_save, sender=Booking)
def update_booking_in_passenger_when_created(sender, instance, created, **kwargs):
    if created:
        # When a new payment is created, set ReadyForBooking to True
        instance.passenger.Booked = True
        instance.passenger.save()

@receiver(pre_delete, sender=Payment)
def update_payment_in_passengerwhen_deleted(sender, instance, **kwargs):
    # Check if the associated Passenger has any other payments
    passenger = instance.passenger
    other_payments_exist = Payment.objects.filter(passenger=passenger).exclude(id=instance.id).exists()

    # If no other payments exist, set ReadyForBooking to False
    if not other_payments_exist:
        passenger.Paid = False
        passenger.save()

@receiver(pre_delete, sender=Booking)
def update_booking_in_passengerwhen_deleted(sender, instance, **kwargs):
    # Check if the associated Passenger has any other payments
    passenger = instance.passenger
    other_payments_exist = Payment.objects.filter(passenger=passenger).exclude(id=instance.id).exists()

    # If no other payments exist, set ReadyForBooking to False
    if not other_payments_exist:
        passenger.Booked = False
        passenger.save()