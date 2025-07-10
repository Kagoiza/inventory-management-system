from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db import transaction
from .models import ItemRequest

# --------------------------
# ✅ Logic Functions
# --------------------------

def can_request_item(user, item, quantity):
    """
    Check whether an item can be requested or not.
    Returns (True, "") if valid, otherwise (False, reason)
    """
    if item.quantity < quantity:
        return False, "Not enough stock available."

    if item.condition == "Poor":
        return False, "Item is not in a usable condition."

    if hasattr(item, 'expiration_date') and item.expiration_date:
        if item.expiration_date < timezone.now().date():
            return False, "This item has expired."

    existing_pending = ItemRequest.objects.filter(requestor=user, item=item, status='Pending')
    if existing_pending.exists():
        return False, "You already have a pending request for this item."

    return True, ""


def approve_item_request(item_request):
    """
    Approve a request and deduct stock. Only allowed if status is Pending and stock is available.
    Returns (True, message) or (False, error)
    """
    if item_request.status != "Pending":
        return False, "Only pending requests can be approved."

    if item_request.item.quantity < item_request.quantity:
        return False, "Insufficient stock to approve request."

    try:
        with transaction.atomic():
            item_request.status = "Approved"
            item_request.item.quantity -= item_request.quantity
            item_request.item.save()
            item_request.save()
        return True, "Request approved and stock updated."
    except Exception as e:
        return False, f"Error approving request: {e}"


def reject_item_request(item_request):
    """
    Reject a pending request without touching stock.
    Returns (True, message) or (False, error)
    """
    if item_request.status != "Pending":
        return False, "Only pending requests can be rejected."

    try:
        item_request.status = "Rejected"
        item_request.save()
        return True, "Request rejected."
    except Exception as e:
        return False, f"Error rejecting request: {e}"


# --------------------------
# ✅ Store Clerk Views
# -----------------------
