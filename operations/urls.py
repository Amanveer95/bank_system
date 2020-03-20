from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.BankCustomers.as_view(), name="customers"),
    path('deposit', views.Deposit.as_view(), name="deposits"),
    path('withdrawal', views.Withdrawal.as_view(), name="withdrawal"),
    path('enquiry', views.Enquiry.as_view(), name="enquiry"),
]