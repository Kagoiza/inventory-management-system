from django.db.models import Q, Sum, F, Count
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth.models import Group

import json
import openpyxl

from .forms import (
    CustomCreationForm,
    ItemRequestForm,
    InventoryItemForm,
    IssueItemForm,
    AdjustStockForm
)

from .models import (
    ItemRequest,
    InventoryItem,
    StockTransaction
)


def register(request):
    if request.method == 'POST':
        form = CustomCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('requestor_dashboard')
    else:
        form = CustomCreationForm()
    return render(request, 'invent/register.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                return redirect('store_clerk_dashboard')
            else:
                return redirect('requestor_dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'invent/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


@login_required
def requestor_dashboard(request):
    user_requests = ItemRequest.objects.filter(requestor=request.user).order_by('-date_requested')
    available_inventory = [item for item in InventoryItem.objects.all().order_by('name') if item.quantity_remaining() > 0]

    return render(request, 'invent/requestor_dashboard.html', {
        'requests': user_requests,
        'total_requests': user_requests.count(),
        'approved_count': user_requests.filter(status='Approved').count(),
        'pending_count': user_requests.filter(status='Pending').count(),
        'available_inventory': available_inventory,
    })


@login_required
def request_item(request):
    item_id_from_get = request.GET.get('item')

    available_inventory_queryset = InventoryItem.objects.all().order_by('name')
    available_inventory_list = [
        item for item in available_inventory_queryset if item.quantity_remaining() > 0
    ]

    available_item_ids = [item.id for item in available_inventory_list]
    filtered_inventory_queryset = InventoryItem.objects.filter(id__in=available_item_ids).order_by('name')

    available_inventory_json = mark_safe(json.dumps([
        {
            "id": item.id,
            "quantity_remaining": item.quantity_remaining(),
            "condition": item.condition or "N/A"
        }
        for item in available_inventory_list
    ]))

    if request.method == 'POST':
        form = ItemRequestForm(request.POST)
        form.fields['item'].queryset = filtered_inventory_queryset

        if form.is_valid():
            try:
                with transaction.atomic():
                    item_request = form.save(commit=False)
                    item = item_request.item
                    item_locked = InventoryItem.objects.select_for_update().get(id=item.id)

                    existing_request = ItemRequest.objects.filter(
                        item=item,
                        requestor=request.user,
                        status='Pending'
                    ).exists()

                    if existing_request:
                        form.add_error('item', "You already have a pending request for this item.")
                        raise forms.ValidationError("Duplicate pending request.")

                    if item_request.quantity > item_locked.quantity_remaining():
                        form.add_error('quantity', f"Only {item_locked.quantity_remaining()} left in stock.")
                        raise forms.ValidationError("Requested quantity exceeds available stock.")

                    item_request.requestor = request.user
                    item_request.name = item.name
                    item_request.save()

                    # ✅ Send email notification
                    send_mail(
                        subject='Item Request Confirmation',
                        message=(
                            f"Dear {request.user.first_name or request.user.username},\n\n"
                            f"Your request for item \"{item_request.item.name}\" has been successfully submitted.\n"
                            f"We will notify you once it is reviewed or issued.\n\n"
                            f"Thank you,\nInventory Management Team"
                        ),
                        from_email=None,  # Uses DEFAULT_FROM_EMAIL
                        recipient_list=[request.user.email],
                        fail_silently=False,
                    )

                    messages.success(request, "Item request submitted successfully!")
                    return redirect('requestor_dashboard')

            except forms.ValidationError:
                pass  # fall through to render form with errors
            except Exception as e:
                messages.error(request, f"Error submitting request: {str(e)}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ItemRequestForm()
        form.fields['item'].queryset = filtered_inventory_queryset

    return render(request, 'invent/request_item.html', {
        'form': form,
        'available_inventory_json': available_inventory_json,
    })
