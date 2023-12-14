from django.db import models
from django.contrib.auth.models import User

class AccountDetails(models.Model):
    account_no = models.PositiveIntegerField(unique=True)
    gender = models.CharField(max_length=50)
    birth_date = models.IntegerField(null=True, blank=True)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return str(self.account_no)

class BankAccount(models.Model):
    account_type = models.CharField(max_length=100)
    minimum_withdrawal_amount = models.IntegerField(default=0)
    maximum_withdrawal_amount = models.IntegerField(default=1000)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    loan_interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5.0)  # Added loan interest rate
    date = models.DateField()
    time = models.TimeField()
    def __str__(self):
        return self.account_type


class Transaction(models.Model):
    date = models.DateField()
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=[('deposit', 'Deposit'), ('withdrawal', 'Withdrawal')])
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending')
    reference_number = models.CharField(max_length=50, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='INR')

    def __str__(self):
        return f"{self.date} - {self.bank_account} - {self.transaction_type} - {self.amount} {self.currency}"

class Withdrawal(models.Model):
    date = models.DateField()
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    withdrawal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='INR')
    

class Deposit(models.Model):
    date = models.DateField()
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='INR')

   
        
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.IntegerField()
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username

class UserAddress(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=512)
    city = models.CharField(max_length=256)
    postal_code = models.PositiveIntegerField()
    country = models.CharField(max_length=256)

    def __str__(self):
        return self.street_address

class Register(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    accountholder = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    accountnumber = models.IntegerField()
    fathername = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phonenumber = models.CharField(max_length=15)
    address = models.TextField()
    pincode = models.IntegerField()

    def __str__(self):
        return self.accountholder

   
   
class Cashier(models.Model):
    cashier_id=models.CharField(max_length=100)
    date = models.DateField()
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=[('deposit', 'Deposit'), ('withdrawal', 'Withdrawal')])
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending')
    reference_number = models.CharField(max_length=50, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='INR')

    def __str__(self):
        return f"{self.date} - {self.bank_account} - {self.transaction_type} - {self.amount} {self.currency}"



# Create your models here.
class FinancialRecord(models.Model):
    principal_amount = models.FloatField()
    annual_interest_rate = models.FloatField()
    compounding_frequency = models.IntegerField()
    time_period_years = models.FloatField()