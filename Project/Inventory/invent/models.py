# C:\Users\Bumi\OneDrive\Documents\Projects\inventory-management-system\Project\Inventory\invent\models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=0) # This 'quantity' might be for the abstract 'Item', not inventory stock

    def __str__(self):
        return self.name

class ItemRequest(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE) 
    type = models.CharField(max_length=100) 
    application_date = models.DateField(default=timezone.now) 

    requestor = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        # Consider adding 'Issued' status here if a request can be marked as fulfilled
    ], default='Pending')
    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name} by {self.requestor.username}"
    

class InventoryItem(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'), # Likely for items awaiting initial approval/stocking
        ('In Stock', 'In Stock'), # Better name than 'Approved' for an inventory item's general status
        ('Issued', 'Issued'),
        ('Returned', 'Returned'), # For items that have been returned but might need inspection
        ('Low Stock', 'Low Stock'), # You could implement logic to set this
        ('Out of Stock', 'Out of Stock'), # You could implement logic to set this
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, blank=True)
    # The 'status' field here is for the overall item state, not transaction state.
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='In Stock') # Changed default to 'In Stock'
    expiration_date = models.DateField(null=True, blank=True)
    quantity_total = models.PositiveIntegerField(default=0) # Total physical items
    quantity_issued = models.PositiveIntegerField(default=0) # Items currently out
    quantity_returned = models.PositiveIntegerField(default=0) # Items returned (may need re-integration into total)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='inventory_created_by') # Added related_name for clarity

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) # Added updated_at for tracking changes

    def __str__(self):
        return f"{self.name} ({self.quantity_total} in total)"

    def is_expired(self):
        return self.expiration_date and self.expiration_date < timezone.now().date()

    def quantity_remaining(self):
        """Calculates the quantity currently available for new issues."""
        return self.quantity_total - self.quantity_issued


# --- NEW MODEL: StockTransaction ---
class StockTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('Issue', 'Issue'),
        ('Adjustment', 'Adjustment'),
        ('Return', 'Return'), # For items returned by users
        ('Receive', 'Receive'), # For new stock coming into inventory
    ]

    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='stock_transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    quantity = models.IntegerField() # Can be positive (add) or negative (remove)
    
    # Optional fields based on transaction type
    issued_to = models.CharField(max_length=255, blank=True, null=True, help_text="Recipient for 'Issue' transactions")
    reason = models.TextField(blank=True, null=True, help_text="Reason for 'Adjustment' or 'Return' transactions")
    
    transaction_date = models.DateTimeField(auto_now_add=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='recorded_transactions')

    def __str__(self):
        action = "added" if self.quantity > 0 else "removed"
        return f"{self.item.name} - {self.transaction_type}: {abs(self.quantity)} ({action}) by {self.recorded_by.username} on {self.transaction_date.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-transaction_date'] # Order by most recent transaction
        # Define custom permissions for more granular control if needed
        permissions = [
            ("can_issue_item", "Can issue inventory items"),
            ("can_adjust_stock", "Can adjust inventory stock"),
            ("can_receive_stock", "Can receive new stock into inventory"),
        ]