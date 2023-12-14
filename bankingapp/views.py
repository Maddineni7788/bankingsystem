from django.shortcuts import render
from django.http import HttpResponse
from bankingapp.models import Register
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.core.mail import send_mail
from django.shortcuts import render, redirect
import random
from django.urls import reverse
from django.shortcuts import  redirect
from bankingapp.models import Transaction,BankAccount,Cashier,Withdrawal,Deposit

from decimal import Decimal

def display(request):
    x=Transaction.objects.all()
    return render(request,'display.html',{'x':x})
def index(request):
    return render(request,'index.html')
def deposit(request):
    return render(request,'deposit.html')  
def withdrawmoney(request):
    return render(request,'deposit.html')  

# Create your views here.
def send_otp(email, otp):
    subject = 'OTP Verification'
    message = f'Your OTP for registration is: {otp}'
    send_mail(subject, message, None, [email])


from django.http import HttpResponseRedirect

# ...

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        accountnumber =request.POST["accountnumber"]
        fathername =request.POST["fathername"]
        dob =request.POST["dob"]
        gender =request.POST["gender"]
        phonenumber =request.POST["phonenumber"]
        address =request.POST["address"]
        pincode =request.POST["pincode"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "accountholder already taken")
            return redirect('registration:register')

        otp_number = random.randint(1000, 9999)
        otp = str(otp_number)

        send_otp(email, otp)
        request.session['username'] = username
        request.session['email'] = email
        request.session['password'] = password
        request.session['otp'] = otp  # Add this line to store OTP in the session

        # Construct the URL using HttpResponseRedirect
        #return HttpResponseRedirect(f'/otp/{otp}/{username}/{password}/{email}/')
        # Alternatively, you can use reverse:
        return HttpResponseRedirect(reverse('bankingapp:otp', args=[otp, username, password, email]))

    else:
        return render(request, 'register.html')


def otp(request, otp, username, password, email):
    if request.method == "POST":
        uotp = request.POST['uotp']
        otp_from_session = request.session.get('otp')

        if uotp == otp_from_session:
            username = request.session.get('username')
            email = request.session.get('email')
            password = request.session.get('password')

            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return redirect('bankingapp:login')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('bankingapp:otp', otp=otp, username=username, password=password, email=email)

    return render(request, 'otp.html',{'otp': otp, 'username': username, 'password': password, 'email': email})



def login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('bankingapp:cashier_mainpage')
        else:
            messages.info(request,'Invalid user credentials')
            return redirect('bankingapp:login')
    else:
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')


from decimal import Decimal
from django.shortcuts import render, redirect
from .models import BankAccount, Transaction

def create_transaction(request):
    bank_accounts = BankAccount.objects.all()
    #transaction_types = Transaction._meta.get_field('transaction_type').choices
    transaction_types = Transaction.objects.all()
    if request.method == "POST":
        date = request.POST.get('date')
        bank_account_id = request.POST.get('bank_account')
        transaction_type = request.POST.get('transaction_type')
        status = request.POST.get('status')
        reference_number = request.POST.get('reference_number')
        amount = Decimal(request.POST.get('amount', 0))
        currency = request.POST.get('currency')

        transaction = Transaction(
            date=date,
            bank_account_id=bank_account_id,
            transaction_type=transaction_type,
            status=status,
            reference_number=reference_number,
            amount=amount,
            currency=currency
        )
        transaction.save()

        # Redirect to a success page or another relevant view
        return HttpResponse("sucess")

    return render(request, 'create_transaction.html', {'bank_accounts': bank_accounts, 'transaction_types': transaction_types})

def cash(request):
    bank_accounts = BankAccount.objects.all()

    if request.method == "POST":
        date = request.POST.get('date')
        bank_account_id = request.POST.get('bank_account')
        transaction_type = request.POST.get('transaction_type')
        status = request.POST.get('status')
        reference_number = request.POST.get('reference_number')
        amount = Decimal(request.POST.get('amount', 0))
        currency = request.POST.get('currency')

        # Create a Cashier instance
        cashier_instance = Cashier(
            date=date,
            bank_account_id=bank_account_id,
            transaction_type=transaction_type,
            status=status,
            reference_number=reference_number,
            amount=amount,
            currency=currency
        )
        # Save the instance to the database
        cashier_instance.save()

        # Redirect to a success page or another relevant view
        return HttpResponse("success")

    return render(request, 'create_transaction.html', {'bank_accounts': bank_accounts})
from django.db.models import Sum

from django.shortcuts import get_object_or_404
from django.db.models import Sum

# def report(request):
#     bank_accounts = BankAccount.objects.all()

#     # Get the specific Cashier instance based on cashier_id
#     cashier_instance = get_object_or_404(Cashier, cashier_id=2)
#     if cashier_instance.transaction_type == 'withdrawal':
#         removed = Cashier.objects.aggregate(count=Sum('amount'))
#         print(removed)
#         print('1')
#     elif cashier_instance.transaction_type == 'deposit':
#         added = Cashier.objects.aggregate(count=Sum('amount'))
#         print("------------------------")
#         print(added)

#     return render(request, 'report.html', {'bank_accounts': bank_accounts})
from django.shortcuts import render
from .models import Cashier, BankAccount
from django.db.models import Sum
from django.db.models import Sum
from .models import BankAccount, Withdrawal, Deposit

def report(request):
    bank_accounts = BankAccount.objects.all()
    d = Deposit.objects.all()
    w = Withdrawal.objects.all()


    # Calculate the total amount for all withdrawals
    total_withdrawals = Withdrawal.objects.aggregate(total=Sum('withdrawal_amount'))['total'] or 0
    print("Total Withdrawals:", total_withdrawals)

    # Calculate the total amount for all deposits
    total_deposits = Deposit.objects.aggregate(total=Sum('deposit_amount'))['total'] or 0
    print("Total Deposits:", total_deposits)

    # Alternatively, if you want to calculate total withdrawals and deposits for each date
    withdrawal_data = Withdrawal.objects.values('date').annotate(total=Sum('withdrawal_amount'))
    deposit_data = Deposit.objects.values('date').annotate(total=Sum('deposit_amount'))

    print("Withdrawals by Date:")
    for item in withdrawal_data:
        print(f"{item['date']} - {item['total']}")

    print("Deposits by Date:")
    for item in deposit_data:
        print(f"{item['date']} - {item['total']}")

    actual_amount=2500000
    amount=total_deposits-total_withdrawals

    added_amount=actual_amount+amount
    return render(request, 'report.html', {'added_amount':added_amount,'bank_accounts': bank_accounts,'d':d,'w':w,'total_withdrawals':total_withdrawals,'total_deposits':total_deposits,'actual_amount':actual_amount,'amount':amount})




def withdrawal(request):
    bank_accounts = BankAccount.objects.all()
    s = Withdrawal.objects.all()

    if request.method == "POST":
        date = request.POST.get('date')
        bank_account_id = request.POST.get('bank_account')  # Assuming 'bank_account' is the ID of the selected bank account
        account_number = request.POST.get('account_number')
        withdrawal_amount = Decimal(request.POST.get('withdrawal_amount', 0))
        currency = request.POST.get('currency')

        # Retrieve the BankAccount instance based on the provided ID
        bank_account = get_object_or_404(BankAccount, id=bank_account_id)

        w = Withdrawal(
            date=date,
            bank_account=bank_account,
            account_number=account_number,
            withdrawal_amount=withdrawal_amount,
            currency=currency
        )
        w.save()
        # Redirect to a success page or another relevant view
        return HttpResponse("success")

    return render(request, 'withdrawal.html', {'bank_accounts': bank_accounts, 's': s})
from django.shortcuts import get_object_or_404

def deposit(request):
    bank_accounts = BankAccount.objects.all()
    t = Deposit.objects.all()

    if request.method == "POST":
        date = request.POST.get('date')
        bank_account_id = request.POST.get('bank_account')  # Assuming 'bank_account' is the ID of the selected bank account
        account_number = request.POST.get('account_number')
        deposit_amount = Decimal(request.POST.get('deposit_amount', 0))
        currency = request.POST.get('currency')

        # Retrieve the BankAccount instance based on the provided ID
        selected_bank_account = get_object_or_404(BankAccount, id=bank_account_id)

        d = Deposit(
            date=date,
            bank_account=selected_bank_account,
            account_number=account_number,
            deposit_amount=deposit_amount,
            currency=currency
        )
        d.save()
        # Redirect to a success page or another relevant view
        return HttpResponse("success")

    return render(request, 'deposit.html', {'bank_accounts': bank_accounts, 't': t})

def cashier_report(request):
    return render(request,'cashier_report.html')

def cashier_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('bankingapp:cashier_mainpage')
        else:
            messages.error(request, 'Invalid user credentials')
            return redirect('bankingapp:cashier_login')
    else:
        return render(request, 'login.html')
def cashier_register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["pass2"]

        if password == password2:
            user = User.objects.create_user(username=username, email=email, password=password)
            
            # Optionally, you might want to automatically log in the user after registration
            login(request, user)
            
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('bankingapp:index')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('bankingapp:cashier_register')
    else:
        return render(request, 'cashier_register.html')

def cashier_mainpage(request):
    return render(request,'cashier_mainpage.html')

# views.py

from django.shortcuts import render
from .forms import FinancialRecordForm

def calculate_interest(request):
    if request.method == 'POST':
        form = FinancialRecordForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            principal_amount = data['principal_amount']
            annual_interest_rate = data['annual_interest_rate']
            compounding_frequency = data['compounding_frequency']
            time_period_years = data['time_period_years']

            # Perform the interest calculation
            n = compounding_frequency
            r = annual_interest_rate / 100  # Convert percentage to decimal
            t = time_period_years

            future_value = principal_amount * (1 + r / n) ** (n * t)

            return render(request, 'result.html', {'future_value': future_value,'principal_amount':principal_amount})
    else:
        form = FinancialRecordForm()

    return render(request, 'calculate_interest.html', {'form': form})
