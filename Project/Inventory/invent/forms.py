# invent/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ItemRequest, Item, InventoryItem, StockTransaction # <-- IMPORTANT: Add StockTransaction here!

class CustomCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ItemRequestForm(forms.ModelForm):
    class Meta:
        model = ItemRequest
        fields = ['quantity', 'reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }



class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['name', 'category', 'status', 'expiration_date', 'quantity_total', 'quantity_issued', 'quantity_returned']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item Name'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category'}),
            'status': forms.Select(attrs={'class': 'form-select'}, choices=InventoryItem.STATUS_CHOICES),
            'expiration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
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
            self.add_error('quantity_issued', 'Quantity issued cannot be greater than total quantity.')
        
        # This validation assumes returned items are part of the 'issued' count initially.
        # If returned items reduce 'quantity_issued' then this validation is tricky.
        # It's better if `quantity_returned` is a separate count, and `quantity_issued` represents *currently out*.
        # If quantity_returned means "items that were issued and are now back", then quantity_issued should *decrease*.
        # For now, keeping the validation as is, but be mindful of the logic.
        if quantity_returned is not None and quantity_issued is not None and quantity_returned > quantity_issued:
             # This specific validation might need to be re-evaluated based on your exact desired stock logic
             # e.g., if quantity_issued is "currently issued out" and returned means "now back in stock"
            self.add_error('quantity_returned', 'Quantity returned cannot be greater than quantity issued.')
        
        # Add a check: total_in_stock (quantity_total - quantity_issued + quantity_returned) should not be negative
        # You have a quantity_remaining property on the model, but for form validation you might want to recalculate
        
        return cleaned_data

# --- NEW: Forms for Stock Operations ---

class IssueItemForm(forms.Form): # This is a regular forms.Form, not ModelForm directly
    item = forms.ModelChoiceField(
        queryset=InventoryItem.objects.filter(quantity_total__gt=0).order_by('name'), # Only show items with some total stock
        empty_label="Select an item",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity to issue'})
    )
    issued_to = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Recipient (e.g., Department, Name)'})
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional notes'})
    )

    def clean(self):
        cleaned_data = super().clean()
        item = cleaned_data.get('item')
        quantity = cleaned_data.get('quantity')

        if item and quantity:
            # Check if there's enough stock available for issue
            if item.quantity_remaining() < quantity: # Using the quantity_remaining property from your model
                raise forms.ValidationError(
                    f"Not enough stock of {item.name} available. Only {item.quantity_remaining()} units currently available for issue."
                )
        return cleaned_data

class AdjustStockForm(forms.Form): # This is a regular forms.Form, not ModelForm directly
    item = forms.ModelChoiceField(
        queryset=InventoryItem.objects.all().order_by('name'),
        empty_label="Select an item",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    # adjustment_quantity: positive for add, negative for remove
    adjustment_quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity to add/remove (e.g., 5 or -3)'}),
        help_text="Enter a positive number to add stock, or a negative number to remove stock."
    )
    reason = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reason for adjustment (e.g., Damage, Audit, New Stock Arrival)'})
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional notes'})
    )

    def clean(self):
        cleaned_data = super().clean()
        item = cleaned_data.get('item')
        adjustment_quantity = cleaned_data.get('adjustment_quantity')

        if item and adjustment_quantity is not None:
            # Prevent total stock from going negative after adjustment
            if (item.quantity_total + adjustment_quantity) < 0:
                raise forms.ValidationError(
                    f"Adjustment would result in negative total stock. Current total: {item.quantity_total}."
                )
        return cleaned_data