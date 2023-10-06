from django.urls import path
from . import views




urlpatterns =[
    path('',views.index,name='index'),
    path('login',views.login_user,name='login_user'),
    path('logout',views.logout_user,name='logout_user'),
    path('add_customer',views.add_customer,name='add_customer'),
    path('edit_customer/<int:pk>',views.edit_customer,name='edit_customer'),
    path('details/<int:pk>', views.Details, name='details'),
    path('delete/<int:pk>', views.delete, name='delete'),
    path('bookings', views.bookings, name='bookings'),
    path('delete_booking/<int:pk>', views.delete_booking, name='delete_booking'),
    path('payments', views.payments, name = 'payments'),
    path('make_payment/<int:pk>', views.make_payment, name = 'make_payment'),
    path('report_payment', views.report_payment , name = 'report_payment'),
    path('custom_report', views.custom_report , name = 'custom_report'),
    path('add_ticket_no/<int:pk>', views.add_ticket_no , name = 'add_ticket_no'),
    path('delet_payment/<int:pk>', views.delet_payment , name = 'delet_payment'),



    

]
