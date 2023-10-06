from django.shortcuts import render,redirect
# response http
from django.http import HttpResponse

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import CreateCustomerForm, Create_Booking, Create_Payment
from .models import Passenger, Booking,Payment
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import send_mail

from datetime import datetime

from .report import Query_model_by_duration
from django.db.models import Q
from django.db.models import Sum



# Create your views here.
@login_required(login_url='login_user')
def index(request):
        if request.method == 'POST':
            date_str = request.POST.get('date')


            passengers = Passenger.objects.filter(Date_created__date=date_str)

            date = datetime.strptime(date_str, "%Y-%m-%d")
            date = date.strftime("%b. %d, %Y")
            print(date)
            return render(request,'booking_brain/index.html', {'passenger': passengers, 'date': date, 'date_str' : date_str})
        else:
            current_t_d = timezone.now().date()
            date = timezone.now()
            passengers = Passenger.objects.filter(Date_created__date=date)
            date_str = str(date)
            return render(request,'booking_brain/index.html', {'passenger': passengers, 'date':date , 'date_str' : date_str , 'current_t_d': current_t_d})

@login_required(login_url='login_user')
def bookings(request):
    bookings = Booking.objects.all()
    return render(request,'booking_brain/bookings.html', {'booking': bookings})
    
@login_required(login_url='login_user')    
def payments(request):
    payment_methods = ['Ebirr', 'CBE', 'IDA', 'IDB']
    durations = ['day', 'week' , 'month']
    context = {}
    for duration in durations:
            for method in payment_methods:
                queryset = Query_model_by_duration(Payment, duration)
                filtered_queryset = queryset.filter(Payment_method=method)
                total_amount = filtered_queryset.aggregate(Sum('Amount'))['Amount__sum']
                if total_amount:
                    key = f'payments_{duration}_{method.lower()}'
                    context[key] = total_amount
    if request.method == 'POST':
        booking_no = request.POST.get('booking_no')
        try:
            booking = Booking.objects.get(Booking_no=booking_no)
        except Booking.DoesNotExist:
            messages.error(request , 'No Booking found')
            return redirect('payments')

        passenger = booking.passenger

        try:
            payment = Payment.objects.get(passenger=passenger)
        except Payment.DoesNotExist:
            messages.error(request , 'No Payment found')
            passenger = passenger
            booking = booking
            context['passenger'] = passenger
            context['booking'] = booking
            return render(request,'booking_brain/payments.html', context)
        booking_no = booking_no 
        return render(request , 'booking_brain/single_payment.html' ,{'payment': payment, 'booking_no':booking_no})
    else:
        print(context)
        return render(request,'booking_brain/payments.html', context)

def delet_payment(request,pk):
    payment_to_delete  = Payment.objects.get(id=pk)
    payment_to_delete.delete()
    messages.success(request,'Payment deleted successfully')
    return redirect('payments')



@login_required(login_url='login_user')
def make_payment(request,pk):
    passenger = Passenger.objects.get(id=pk)
    booking = Booking.objects.get(passenger=passenger)
    if request.method == 'POST':
        
        form = Create_Payment(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.Ticket_no = None
            payment.passenger = passenger
            payment.save()
            messages.success(request,'Payment added successfully')
            return redirect('payments')
        else:
            
            messages.success(request,'Error occured while adding payment')
            return redirect('make_payment', pk=pk)
    else:
        form = Create_Payment(initial={
            'Amount' : passenger.Amount,
            'Ticket_no' : "0"
        })
        context = {'form':form , 'passenger':passenger, 'booking':booking}
        return render(request,'booking_brain/make_payment.html', context )

def add_ticket_no(request,pk):
    payment_ = Payment.objects.get(id=pk)
    passenger = payment.passenger
    booking_no = Booking.objects.get(passenger=passenger).Booking_no
    if request.method == 'POST':
        form = Create_Payment(request.POST, instance=payment_)
        if form.is_valid():
            payment = form.save(commit=False)
            form.save()
            messages.success(request,'Ticket no added successfully')
            return redirect('payments')
            # return render(request , 'booking_brain/single_payment.html' ,{'payment': payment_, 'booking_no':booking_no})

    else:
        form = Create_Payment(instance=payment)
        context = {'form':form , 'passenger':passenger, 'payment':payment}
        return render(request,'booking_brain/add_ticket_no.html', context )
        



@login_required(login_url='login_user')  
def report_payment(request):
    
    payments_today =  Query_model_by_duration(Payment, 'day')
    today_amount_ea = payments_today.aggregate(Sum('Amount_EA'))['Amount_EA__sum']
    today_amount_z_com = payments_today.aggregate(Sum('Amount_Z_com'))['Amount_Z_com__sum']
    today_amount_m_com = payments_today.aggregate(Sum('Amount_M_com'))['Amount_M_com__sum']
    today_amount = payments_today.aggregate(Sum('Amount'))['Amount__sum']

    payments_this_week =  Query_model_by_duration(Payment, 'week')
    week_amount_ea = payments_this_week.aggregate(Sum('Amount_EA'))['Amount_EA__sum']
    week_amount_z_com = payments_this_week.aggregate(Sum('Amount_Z_com'))['Amount_Z_com__sum']
    week_amount_m_com = payments_this_week.aggregate(Sum('Amount_M_com'))['Amount_M_com__sum']
    week_amount = payments_this_week.aggregate(Sum('Amount'))['Amount__sum']

    payments_this_month  = Query_model_by_duration(Payment, 'month')
    month_amount_ea = payments_this_month.aggregate(Sum('Amount_EA'))['Amount_EA__sum']
    month_amount_z_com = payments_this_month.aggregate(Sum('Amount_Z_com'))['Amount_Z_com__sum']
    month_amount_m_com = payments_this_month.aggregate(Sum('Amount_M_com'))['Amount_M_com__sum']
    month_amount = payments_this_month.aggregate(Sum('Amount'))['Amount__sum']

    context = {
        'payments_today' : {'objects' : payments_today, 'amount_ea' : today_amount_ea, 
        'amount_m_com' : today_amount_m_com, 'amount_z_com' : today_amount_z_com, 'amount' : today_amount},                  
        'payments_this_week' : {'objects' : payments_this_week, 'amount_ea' : week_amount_ea, 
        'amount_m_com' : week_amount_m_com, 'amount_z_com' : week_amount_z_com, 'amount' : week_amount},
        'payments_this_month' : {'objects' : payments_this_month, 'amount_ea' : month_amount_ea, 
        'amount_m_com' : month_amount_m_com, 'amount_z_com' : month_amount_z_com, 'amount' : month_amount}
    }
    
  
    return render(request,'booking_brain/report_payment.html', context)

def custom_report(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        filtered_objects = Payment.objects.filter(
        Q(Date_created__gte=start_date) & Q(Date_created__lte=end_date)
        )
        if filtered_objects:
            custom_objects = filtered_objects
            custom_objects_ea = custom_objects.aggregate(Sum('Amount_EA'))['Amount_EA__sum']
            custom_objects_z_com = custom_objects.aggregate(Sum('Amount_Z_com'))['Amount_Z_com__sum']
            custom_objects_m_com = custom_objects.aggregate(Sum('Amount_M_com'))['Amount_M_com__sum']
            custom_objects_amount = custom_objects.aggregate(Sum('Amount'))['Amount__sum']
            context = {'payments':custom_objects, 'custom_objects_ea' : custom_objects_ea,
                       'custom_objects_z_com': custom_objects_z_com, 'custom_objects_m_com' : custom_objects_m_com,
                       'custom_objects_amount' : custom_objects_amount}

            return render(request,'booking_brain/custom_report.html', context)

    else:

        return render(request,'booking_brain/custom_report.html')

@login_required(login_url='login_user')
def report(request):
    pass
@login_required(login_url='login_user')
def add_customer(request):
    if request.method == 'POST':
        form = CreateCustomerForm(request.POST)
        if form.is_valid():
            passenger = form.save(commit=False)
            passenger.user = request.user
            passenger.save()
            messages.success(request,'Customer added successfully')
            return redirect('index')
        
        else:
            messages.success(request,'Error occured while adding customer')
            
            return redirect('add_customer')
    else:
        form = CreateCustomerForm()
        context = {'form':form}
        return render(request,'booking_brain/add_customer.html', context )

@login_required(login_url='login_user')
def edit_customer(request,pk):
    passenger = Passenger.objects.get(id=pk)
    if request.method == 'POST':
        form = CreateCustomerForm(request.POST, instance=passenger)
        if form.is_valid():
            passenger = form.save(commit=False)
            passenger.user = request.user
            passenger.save()
            messages.success(request,'Customer updated successfully')
            return redirect('index')
        else:
            messages.success(request,'Error occured while updating customer')
            return redirect('edit_customer',pk=pk)
    else:
        form = CreateCustomerForm(instance=passenger)
        context = {'form':form}
        return render(request,'booking_brain/edit_customer.html', context )

@login_required(login_url='login_user')
def Details(request,pk):
    passenger = Passenger.objects.get(id=pk)
    if request.method == 'POST':
        form = Create_Booking(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.passenger = passenger
            booking.user = request.user
            booking.save()
            messages.success(request,'Booking added successfully')
            ## stay same page
            return redirect('details',pk=pk)
        

        else:
            messages.error(request, "Couldnot saved")
            return redirect('details',pk=pk)
 
    else:
        form = Create_Booking()
        passenger = Passenger.objects.get(id=pk)
        booking =  Booking.objects.filter(passenger=passenger).exists()
        if booking:
            booking = Booking.objects.get(passenger=passenger)
            context = {'passenger':passenger,'form':form,'booking':booking}
            return render(request,'booking_brain/details.html', context)
        else:
            context = {'passenger':passenger,'form':form}
            return render(request,'booking_brain/details.html', context)




        



        
        
        
        # else:  
        #     context = {'passenger':passenger,'form':form}
        #     return render(request,'booking_brain/details.html', context)

@login_required(login_url='login_user')
def delete(request,pk):
    passenger_to_delete = Passenger.objects.filter(id=pk)
    passenger_to_delete.delete()
    return redirect('index')
def delete_booking(request,pk):
    booking_to_delete = Booking.objects.filter(id=pk)
    passenger = Booking.objects.get(id=pk).passenger.id
    booking_to_delete.delete()
    return redirect('details',pk=passenger)

    
   


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'Logged in successfully')
            return redirect('index')
        else:
            messages.success(request,'Username or Password is incorrect')
            return redirect('login_user')
    else:
        return render(request,'booking_brain/login.html')

def logout_user(request):
    logout(request)
    messages.success(request,'Logged out successfully')
    return redirect('login_user')

def create_user(resquest):
    pass        
