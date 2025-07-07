from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class ItemRequest(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  # Item ID
    type = models.CharField(max_length=100)           # Type of request
    application_date = models.DateField(default=timezone.now)    # Date auto-set

    requestor = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ], default='Pending')
    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name} by {self.requestor.username}"
    

class InventoryItem(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Issued', 'Issued'),
        ('Returned', 'Returned'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, blank=True)  # Optional
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    expiration_date = models.DateField(null=True, blank=True)
    quantity_total = models.PositiveIntegerField(default=0)
    quantity_issued = models.PositiveIntegerField(default=0)
    quantity_returned = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.status})"

    def is_expired(self):
        from django.utils import timezone
        return self.expiration_date and self.expiration_date < timezone.now().date()

    def quantity_remaining(self):
        return self.quantity_total - self.quantity_issued + self.quantity_returned

