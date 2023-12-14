# forms.py

from django import forms
from .models import FinancialRecord

class FinancialRecordForm(forms.ModelForm):
    class Meta:
        model = FinancialRecord
        fields = ['principal_amount', 'annual_interest_rate', 'compounding_frequency', 'time_period_years']
