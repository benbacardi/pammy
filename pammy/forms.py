'''Pammy forms'''
from django import forms

from .models import Allocation

class AllocationForm(forms.ModelForm):
    class Meta:
        model = Allocation
        fields = ['network', 'name']

class DivideForm(forms.Form):
    def __init__(self, allocation):
        self.allocation = allocation
