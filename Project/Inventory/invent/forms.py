# invent/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ItemRequest
from .models import Item

class CustomCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class RequestItemForm(forms.ModelForm):
    class Meta:
        model = ItemRequest
        fields = ['item', 'type']  # Make sure field names match your model
        widgets = {
            'item': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'item': 'Item ID',
            'type': 'Type',
        }



class ManageStockForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'quantity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }
        labels = {
            'name': 'Item Name',
            'description': 'Description',
            'quantity': 'Quantity in Stock',
        }
