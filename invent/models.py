# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import send_mail


class InventoryItem(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Stock', 'In Stock'),
        ('Issued', 'Issued'),
        # This can be used if an entire *type* of item is deemed 'returned' for some reason,
        ('Returned', 'Returned'),
        # or if you track individual serial numbers and this field applies to each serial.
        # For aggregate quantities, 'In Stock', 'Low Stock', 'Out of Stock' are more common.
        ('Low Stock', 'Low Stock'),
        ('Out of Stock', 'Out of Stock'),
    ]

    CONDITION_CHOICES = [
        ("Serviceable", "Serviceable"),
        ("Not Serviceable", "Not Serviceable"),
        ("Not working", "Not working"),
        ("Good", "Good"),
        ("Fair", "Fair"),
        ("Poor", "Poor"),
    ]

    name = models.CharField(
        max_length=255, help_text="e.g., Dell Optiplex 7010 (from Asset Description)")
    serial_number = models.CharField(
        max_length=255, unique=True, blank=True, null=True,
        help_text="Unique serial number of the asset (from Serial Number in CSV)"
    )
    category = models.CharField(
        max_length=100, blank=True,
        help_text="e.g., Printer, CPU, Monitor (from Asset Category-Minor)"
    )
    condition = models.CharField(
        max_length=20, choices=CONDITION_CHOICES, default="Serviceable",
        help_text="Current condition of the asset (from Condition in CSV)"
    )

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='In Stock')
    expiration_date = models.DateField(null=True, blank=True)
    quantity_total = models.PositiveIntegerField(default=0)
    quantity_issued = models.PositiveIntegerField(default=0)
    # This field is for *aggregate* returns of this item type.
    quantity_returned = models.PositiveIntegerField(default=0)
    # Actual returns are handled via StockTransaction and ItemRequest.

    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='inventory_created_by')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # If serial_number is truly unique per physical item, then quantity_total etc. would be 1 for each object.
        # If it's a type of item, then serial_number should not be unique and quantity_total would be > 1.
        # Assuming for now it's a type of item with an optional unique serial for individual units if desired.
        # This string representation is better for unique items.
        return f"{self.name} (S/N: {self.serial_number or 'N/A'})"
        # If it's a type, it might be just `self.name`.

    def is_expired(self):
        return self.expiration_date and self.expiration_date < timezone.now().date()

    def quantity_remaining(self):
        """Calculates the quantity currently available for new issues."""
        return self.quantity_total - self.quantity_issued


class ItemRequest(models.Model):
    item = models.ForeignKey('InventoryItem', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)  # Quantity requested
    reason = models.TextField(blank=True, null=True)
    application_date = models.DateField(default=timezone.now)
    requestor = models.ForeignKey(User, on_delete=models.CASCADE)

    # UPDATED STATUS CHOICES for ItemRequest
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Issued', 'Issued'),  # Item has been issued (fully or partially)
        ('Rejected', 'Rejected'),
        ('Cancelled', 'Cancelled'),
        # Some but not all issued quantity returned
        ('Partially Returned', 'Partially Returned'),
        # All issued quantity for this request has been returned
        ('Fully Returned', 'Fully Returned'),
    ]
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Pending')  # Increased max_length

    date_requested = models.DateTimeField(auto_now_add=True)
    # To track when it was actually issued
    date_issued = models.DateTimeField(null=True, blank=True)

    # NEW FIELD: To track how much of this specific request has been returned
    returned_quantity = models.PositiveIntegerField(default=0)

    _original_status = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_status = self.status

    def save(self, *args, **kwargs):
        status_changed = self.pk and self.status != self._original_status
        super().save(*args, **kwargs)

        if status_changed:
            subject = None
            message = None
            user = self.requestor

            if self.status == 'Rejected':
                subject = "Item Request Rejected"
                message = (
                    f"Dear {user.first_name or user.username},\n\n"
                    f"Your request for item \"{self.item.name}\" has been rejected.\n"
                    f"If you believe this is an error, please contact the store clerk.\n\n"
                    f"Thank you,\nInventory Management System"
                )
            elif self.status == 'Approved':
                subject = "Item Request Approved"
                message = (
                    f"Dear {user.first_name or user.username},\n\n"
                    f"Your request for item \"{self.item.name}\" has been approved.\n"
                    f"You will be notified once the item is issued.\n\n"
                    f"Thank you,\nInventory Management System"
                )
            elif self.status == 'Issued':
                subject = "Item Issued"
                message = (
                    f"Dear {user.first_name or user.username},\n\n"
                    f"Your item \"{self.item.name}\" has been issued successfully.\n"
                    f"Kindly pick up you item.\n\n"
                    f"Thank you,\nInventory Management System"
                )
                if not self.date_issued:  # Set date_issued only once
                    self.date_issued = timezone.now()
                    # Save date_issued immediately
                    super().save(update_fields=['date_issued'])
            elif self.status == 'Cancelled':
                subject = "Item Request Cancelled"
                message = (
                    f"Dear {user.first_name or user.username},\n\n"
                    f"Your item request for \"{self.item.name}\" has been cancelled.\n\n"
                    f"Regards,\nInventory Management System"
                )
            elif self.status == 'Partially Returned' or self.status == 'Fully Returned':
                subject = f"Item Return Confirmation - Request for {self.item.name}"
                message = (
                    f"Dear {user.first_name or user.username},\n\n"
                    f"The item \"{self.item.name}\" (Quantity: {self.returned_quantity}/{self.quantity}) from your request "
                    f"has been marked as {self.status.lower()} in the system.\n\n"
                    f"Thank you,\nInventory Management System"
                )

            if subject and message:
                send_mail(
                    subject,
                    message,
                    from_email=None,  # Uses DEFAULT_FROM_EMAIL from settings.py
                    recipient_list=[user.email],
                    fail_silently=False,
                )

            self._original_status = self.status  # Update tracker

    def __str__(self):
        return f"Request for {self.item.name} by {self.requestor.username}"

    def quantity_to_be_returned(self):
        """Calculates the quantity that was issued and is not yet returned for this request."""
        return self.quantity - self.returned_quantity


class StockTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('Issue', 'Issue'),
        ('Adjustment', 'Adjustment'),
        ('Return', 'Return'),
        ('Receive', 'Receive'),
    ]

    item = models.ForeignKey(
        InventoryItem, on_delete=models.CASCADE, related_name='stock_transactions')
    transaction_type = models.CharField(
        max_length=20, choices=TRANSACTION_TYPES)
    # Use IntegerField as returns will be negative if you track direction,
    quantity = models.IntegerField()
    # but for returns we'll use positive number and type='Return'

    # Associate transaction with a specific ItemRequest if it's an 'Issue' or 'Return'
    item_request = models.ForeignKey(
        ItemRequest, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='stock_transactions',
        help_text="Link to the original item request if applicable (for Issue/Return transactions)"
    )

    issued_to = models.CharField(
        max_length=255, blank=True, null=True, help_text="Recipient for 'Issue' transactions")
    reason = models.TextField(
        blank=True, null=True, help_text="Reason for 'Adjustment' or 'Return' transactions")

    transaction_date = models.DateTimeField(auto_now_add=True)
    recorded_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='recorded_transactions')

    def __str__(self):
        action = "added" if self.quantity > 0 else "removed"
        # Adjusting the __str__ to be more descriptive for returns
        if self.transaction_type == 'Return':
            return f"{self.item.name} - Returned: {self.quantity} by {self.recorded_by.username} on {self.transaction_date.strftime('%Y-%m-%d')}"
        else:
            return f"{self.item.name} - {self.transaction_type}: {abs(self.quantity)} ({action}) by {self.recorded_by.username} on {self.transaction_date.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-transaction_date']
        permissions = [
            ("can_issue_item", "Can issue inventory items"),
            ("can_adjust_stock", "Can adjust inventory stock"),
            ("can_receive_stock", "Can receive new stock into inventory"),
        ]
