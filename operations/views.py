from django.shortcuts import render
from .models import Customers, Transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

class BankCustomers(APIView):
    def get(self,request):
        users = Customers.objects.all()
        if users:
            user_list = []

            for user in users:
                user_list.append({
                'first_name' : user.first_name,
                'last_name' : user.last_name,
                'age' : user.age,
                'email' : user.email
                })

            return Response(user_list)

        else:
            return Response("No users created. Start adding users")

    def post(self, request):
        try:
            data = request.data
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            age = data.get('age')
            email = data.get('email')

            if first_name != '' and email != '' and age != '':
                new_customer = Customers(
                    first_name=first_name,
                    last_name = last_name,
                    age=age,
                    email=email,
                )
                new_customer.save()

                return HttpResponseRedirect(reverse('customers'))

            else:
                return Response("No user Created. First Name, Email, Age are required")
        except:
            return Response("Unable to create user. Please provide First Name, Email, Age and try again")


class Deposit(APIView):
    def post(self, request):
        try:
            data = request.data
            deposit = data.get('deposit')
            if deposit:
                userid = data.get('userid')

                is_user = Customers.objects.filter(id = userid).first()
                if is_user:
                    net_amount = Transaction.objects.filter(user_id = userid).values('net_amount').order_by('-created_at').first()
                    if net_amount is not None:
                        net_amount = int(net_amount['net_amount']) + deposit
                    else:
                        net_amount = deposit
                    
                    new_transaction = Transaction(
                        user_id = userid,
                        deposit_amount = deposit,
                        net_amount = net_amount,
                    ).save()
                    
                    receiver_email = is_user.email
                    # send_mail("Amount Deposited",
                    # ("Rs {} has been deposited in your account").format(deposit),
                    # "sender email",
                    # ["receiver email"],
                    # fail_silently= False)

                    return Response(('Rs {} has been deposited in you account').format(deposit))
                else:
                    return Response("Please provide correct userid")
            else:
                return Response("Please Enter Deposit Amount")

        except:
            return Response("Please enter deposit amount and userid")


class Withdrawal(APIView):
    def post(self, request):
        try:
            data = request.data
            withdrawal = data.get('withdrawal')
            if withdrawal:
                userid = data.get('userid')

                is_user = Customers.objects.filter(id = userid).first()
                if is_user:
                    net_amount = Transaction.objects.filter(user_id = userid).values('net_amount').order_by('-created_at').first()
                    
                    if net_amount is not None and int(net_amount['net_amount']) > int(withdrawal):
                        
                        net_amount = int(net_amount['net_amount']) - withdrawal
                        
                        new_transaction = Transaction(
                        user_id = userid,
                        withdrawal_amount = withdrawal,
                        net_amount = net_amount,
                        )
                        new_transaction.save()

                        receiver_email = is_user.email
                        # send_mail("Amount Withdrawan",
                        # ("Rs {} has been withdrawn from you account").format(withdrawal),
                        # "sender email",
                        # ["receiver email"],
                        # fail_silently= False)

                        return Response(('your withdrawal of Rs {} is complete').format(withdrawal))
                    
                    else:
                        return Response('You have dont have enough balance')
                else:
                    return Response("Please provide correct userid")
            else:
                return Response("Please enter Withdrawal Amount")
        except:
            return Response("Please enter withdrawal amount and userid")


class Enquiry(APIView):
    def post(self, request):
        try:
            data = request.data
            userid = data.get("userid")
            is_user = Customers.objects.filter(id = userid)
            if is_user:
                balance = Transaction.objects.filter(user_id = userid).values('net_amount').order_by('-created_at').first()

                final_balance = {'balance' : balance['net_amount']}

                return Response(final_balance)

            else:
                return Response("No such user exist. Register User")
        except:
            return Response("Please enter userid")