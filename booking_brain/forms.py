from django import forms
from .models import Passenger, Booking, Payment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm




class CreateCustomerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['First_name', 'Middle_name', 'Last_name', 'Phone_number', 'Departure_place', 'Destination', 'Departure_date', 'Return_date', 'Amount']
        widgets = {
            'First_name': forms.TextInput(attrs={'id':'firstn','class': 'form-control col-6' ,'id':'firstn', 'placeholder': 'First Name' , 'required': True}),
            'Middle_name': forms.TextInput(attrs={'id':'midn','class': 'form-control col-6', 'id':'midn' , 'placeholder': 'Middle Name' , }),
            'Last_name': forms.TextInput(attrs={'id':'lname','class': 'form-control' , 'placeholder': 'Last Name' , 'required': True}),
            'Phone_number': forms.NumberInput(attrs={'type': 'number','class': 'form-control' , 'placeholder': 'Phone Number' , 'required': True}),
            'Departure_place': forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Departure Place' , 'required': True}),
            'Destination': forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Destination' , 'required': True}),
            'Departure_date': forms.DateInput(attrs={"type": "date",'class': 'form-control' , 'placeholder': 'Departure Date' , 'required': True}),
            'Return_date': forms.DateInput( attrs={'type': 'date','class': 'form-control' , 'placeholder': 'Return Date', "required": False }),
            'Amount': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control' , 'placeholder': 'Amount' , 'required': True}),
        }
    

class Create_Booking(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['Passport_country', 'Passport_no', 'Passport_expiry', 'Date_birth', 'Gender']
        widgets = {
            'Passport_country': forms.TextInput(attrs={'class': 'form-control col-6' , 'placeholder': 'Passport Country' , 'required': True}),
            'Passport_no': forms.TextInput(attrs={'class': 'form-control col-6' , 'placeholder': 'Passport Number' , 'required': True}),
            'Passport_expiry': forms.DateInput(attrs={"type": "date",'class': 'form-control' , 'placeholder': 'Passport Expiry' , 'required': True}),
            'Date_birth': forms.DateInput(attrs={"type": "date",'class': 'form-control' , 'placeholder': 'Date of Birth' , 'required': True}),
            'Gender': forms.Select(attrs={'class': 'form-control' , 'placeholder': 'Gender' , 'required': True}, choices=(("",""),("Male","Male"),("Female","Female"))),
        }
        

class Create_Payment(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['Payment_method',  'Payment_ref','Ticket_no', 'Amount_EA','Amount_Z_com','Amount_M_com', 'Amount']
        widgets = {
            'Payment_method': forms.Select(attrs={'class': 'form-control' , 'placeholder': 'Gender' , 'required': True}, choices=(("Ebirr","Ebirr"),("CBE","CBE"),("IDA","IDA"),("IDB","IDB"))),
            'Payment_ref': forms.TextInput(attrs={'class': 'form-control col-6' , 'placeholder': 'Payment Ref' , 'required': True}),
            'Ticket_no' : forms.TextInput(attrs={'class': 'form-control col-6' , 'placeholder': 'Ticket number', }),
            'Amount_EA' : forms.NumberInput(attrs={'id':'Amount_EA', 'type': 'number', 'class': 'form-control' , 'placeholder': 'Ethiopian Airline' , 'required': True}),
            'Amount_M_com' : forms.NumberInput(attrs={'id':'Amount_M_com','type': 'number', 'class': 'form-control' , 'placeholder': 'Merhaba Commision' , 'required': True}),
            'Amount_Z_com' : forms.NumberInput(attrs={'id':'Amount_Z_com','type': 'number', 'class': 'form-control' , 'placeholder': 'Zamzam Commision' , 'required': True}),
            'Amount': forms.NumberInput(attrs={'id':'Amount','type': 'number', 'class': 'form-control' , 'placeholder': 'Total' , 'required': True}),
        }

