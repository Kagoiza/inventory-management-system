from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ItemRequest, InventoryItem, StockTransaction


class CustomCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ItemRequestForm(forms.ModelForm):
    item = forms.ModelChoiceField(
        queryset=InventoryItem.objects.all().order_by('name'),
        label="Select an Item",
        empty_label="-- Select an Item --",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = ItemRequest
        fields = ['item', 'quantity', 'reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }


class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        # UPDATED FIELDS HERE: Added 'serial_number' and 'condition'
        fields = ['name', 'category', 'condition', 'status', 'serial_number',
                  'quantity_total', 'quantity_issued', 'quantity_returned']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item Name'}),
            # Added widget for serial_number
            'serial_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Serial Number'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category'}),
            # Added widget for condition
            'condition': forms.Select(attrs={'class': 'form-select'}, choices=InventoryItem.CONDITION_CHOICES),
            'status': forms.Select(attrs={'class': 'form-select'}, choices=InventoryItem.STATUS_CHOICES),
            'quantity_total': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'quantity_issued': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'quantity_returned': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }

    def clean(self):
        cleaned_data = super().clean()
        quantity_total = cleaned_data.get('quantity_total')
        quantity_issued = cleaned_data.get('quantity_issued')
        quantity_returned = cleaned_data.get('quantity_returned')

        if quantity_issued is not None and quantity_total is not None and quantity_issued > quantity_total:
            self.add_error(
                'quantity_issued', 'Quantity issued cannot be greater than total quantity.')

        if quantity_returned is not None and quantity_issued is not None and quantity_returned > quantity_issued:
            self.add_error(
                'quantity_returned', 'Quantity returned cannot be greater than quantity issued.')

        return cleaned_data


class IssueItemForm(forms.Form):
    item = forms.ModelChoiceField(
        queryset=InventoryItem.objects.filter(
            quantity_total__gt=0).order_by('name'),
        empty_label="Select an item",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(
            attrs={'class': 'form-control', 'placeholder': 'Quantity to issue'})
    )
    issued_to = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Recipient (e.g., Department, Name)'})
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional notes'})
    )

    def clean(self):
        cleaned_data = super().clean()
        item = cleaned_data.get('item')
        quantity = cleaned_data.get('quantity')

        if item and quantity:
            if item.quantity_remaining() < quantity:
                raise forms.ValidationError(
                    f"Not enough stock of {item.name} available. Only {item.quantity_remaining()} units currently available for issue."
                )
        return cleaned_data


class AdjustStockForm(forms.Form):
    item = forms.ModelChoiceField(
        queryset=InventoryItem.objects.all().order_by('name'),
        empty_label="Select an item",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    adjustment_quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={
                                 'class': 'form-control', 'placeholder': 'Quantity to add/remove (e.g., 5 or -3)'}),
        help_text="Enter a positive number to add stock, or a negative number to remove stock."
    )
    reason = forms.CharField(
        widget=forms.TextInput(attrs={
                               'class': 'form-control', 'placeholder': 'Reason for adjustment (e.g., Damage, Audit, New Stock Arrival)'})
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional notes'})
    )

    def clean(self):
        cleaned_data = super().clean()
        item = cleaned_data.get('item')
        adjustment_quantity = cleaned_data.get('adjustment_quantity')

        if item and adjustment_quantity is not None:
            if (item.quantity_total + adjustment_quantity) < 0:
                raise forms.ValidationError(
                    f"Adjustment would result in negative total stock. Current total: {item.quantity_total}."
                )
        return cleaned_data
