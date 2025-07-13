from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Sum, F, Count, Q
from django.db import transaction
from django.http import HttpResponse # Keep HttpResponse for other potential uses, or remove if truly not needed elsewhere
from django.utils import timezone
import json
from django.utils.safestring import mark_safe

# Correct Model and Form Imports
from .models import ItemRequest, InventoryItem, StockTransaction # Removed 'Item' if it's not actually used
from .forms import ItemRequestForm
from .forms import InventoryItemForm
from .forms import IssueItemForm
from .forms import AdjustStockForm

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

    # Fetch available inventory items for the requestor
    # Only show items with a quantity remaining > 0
    available_inventory = [item for item in InventoryItem.objects.all().order_by('name') if item.quantity_remaining() > 0]

    total_requests = user_requests.count()
    approved_count = user_requests.filter(status='Approved').count()
    pending_count = user_requests.filter(status='Pending').count()

    return render(request, 'invent/requestor_dashboard.html', {
        'requests': user_requests,
        'total_requests': total_requests,
        'approved_count': approved_count,
        'pending_count': pending_count,
        'available_inventory': available_inventory, # Pass available inventory (though not directly used by default dashboard content, good to have)
    })

from django.core.mail import send_mail  # Add this at the top

@login_required
def request_item(request):
    item_id_from_get = request.GET.get('item')

    available_inventory_queryset = InventoryItem.objects.all().order_by('name')
    available_inventory_list = [item for item in available_inventory_queryset if item.quantity_remaining() > 0]

    available_item_ids = [item.id for item in available_inventory_list]
    filtered_inventory_queryset = InventoryItem.objects.filter(id__in=available_item_ids).order_by('name')

    # JS-safe JSON data for showing item quantity/condition
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
            item_request = form.save(commit=False)
            item_request.requestor = request.user
            item_request.save()

            # ✅ Send email notification to the requestor
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
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        initial_data = {}
        if item_id_from_get and item_id_from_get.isdigit():
            try:
                item = InventoryItem.objects.get(id=int(item_id_from_get))
                if item.id in available_item_ids:
                    initial_data['item'] = item.id
            except InventoryItem.DoesNotExist:
                pass

        form = ItemRequestForm(initial=initial_data)
        form.fields['item'].queryset = filtered_inventory_queryset

    return render(request, 'invent/request_item.html', {
        'form': form,
        'available_inventory': available_inventory_list,
        'available_inventory_json': available_inventory_json,
    })


@login_required
def cancel_request(request, request_id):
    item_request = get_object_or_404(ItemRequest, id=request_id, requestor=request.user)

    if item_request.status == 'Pending':
        if request.method == 'POST':
            item_request.status = 'Cancelled'
            item_request.processed_by = request.user
            item_request.processed_at = timezone.now()
            item_request.save()
            messages.success(request, f"Request for '{item_request.item.name}' (ID: {request_id}) has been cancelled.")
            return redirect('requestor_dashboard')
        else:
            context = {
                'item_request': item_request
            }
            return render(request, 'invent/cancel_request_confirm.html', context)
    else:
        messages.error(request, f"Request for '{item_request.item.name}' (ID: {request_id}) cannot be cancelled because its status is '{item_request.status}'.")
        return redirect('requestor_dashboard')
    



# --- Store Clerk Functionality ---

@login_required
@permission_required('invent.view_inventoryitem', raise_exception=True)
def store_clerk_dashboard(request):
    inventory_items = InventoryItem.objects.all()

    total_inventory_items = inventory_items.aggregate(total_sum=Sum('quantity_total'))['total_sum'] or 0
    items_issued = inventory_items.aggregate(total_issued=Sum('quantity_issued'))['total_issued'] or 0
    items_returned = inventory_items.aggregate(total_returned=Sum('quantity_returned'))['total_returned'] or 0

    items_for_dashboard = inventory_items.order_by('-created_at')[:5]

    pending_requests_count = ItemRequest.objects.filter(status='Pending').count()

    context = {
        'total_items': total_inventory_items,
        'items_issued': items_issued,
        'items_returned': items_returned,
        'items': items_for_dashboard,
        'pending_requests_count': pending_requests_count,
    }
    return render(request, 'invent/store_clerk_dashboard.html', context)


@login_required
@permission_required('invent.view_inventoryitem', raise_exception=True)
def manage_stock(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.created_by = request.user
            new_item.save()
            messages.success(request, f'Inventory item "{new_item.name}" added successfully.')
            return redirect('manage_stock')
        else:
            messages.error(request, "Error adding item. Please check the form.")
    else:
        form = InventoryItemForm()

    items = InventoryItem.objects.all().order_by('name')

    context = {
        'form': form,
        'items': items,
    }
    return render(request, 'invent/manage_stock.html', context)


@login_required
@permission_required('invent.change_inventoryitem', raise_exception=True)
def edit_item(request, item_id):
    item = get_object_or_404(InventoryItem, id=item_id)
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            if not item.created_by:
                item.created_by = request.user
            form.save()
            messages.success(request, f'Inventory Item "{item.name}" updated successfully!')
            return redirect('manage_stock')
        else:
            messages.error(request, "Error updating item. Please correct the errors below.")
    else:
        form = InventoryItemForm(instance=item)

    context = {
        'form': form,
        'item': item,
    }
    return render(request, 'invent/edit_item.html', context)


@login_required
@permission_required('invent.can_issue_item', raise_exception=True)
def issue_item(request):
    all_requests = ItemRequest.objects.all().order_by('-date_requested')
    pending_and_approved_requests = all_requests.filter(status__in=['Pending', 'Approved'])

    form = IssueItemForm()

    if request.method == 'POST':
        action = request.POST.get('action')
        request_id = request.POST.get('request_id')

        if action and request_id:
            item_request = get_object_or_404(ItemRequest, id=request_id)
            try:
                with transaction.atomic():
                    if action == 'approve':
                        item_request.status = 'Approved'
                        item_request.processed_by = request.user
                        item_request.processed_at = timezone.now()
                        item_request.save()
                        messages.success(request, f"Request ID {request_id} ({item_request.item.name}) approved.")
                    elif action == 'reject':
                        item_request.status = 'Rejected'
                        item_request.processed_by = request.user
                        item_request.processed_at = timezone.now()
                        item_request.save()
                        messages.warning(request, f"Request ID {request_id} ({item_request.item.name}) rejected.")
                    elif action == 'issue_from_request':
                        if item_request.status not in ['Pending', 'Approved']:
                            messages.error(request, f"Cannot issue for request ID {request_id}. Status is '{item_request.status}'.")
                            return redirect('issue_item')

                        item_to_issue_obj = item_request.item

                        if item_to_issue_obj.quantity_remaining() < item_request.quantity:
                            messages.error(request, f"Insufficient stock for '{item_to_issue_obj.name}'. Requested: {item_request.quantity}, Available: {item_to_issue_obj.quantity_remaining()}.")
                            return redirect('issue_item')

                        item_to_issue_obj.quantity_issued = F('quantity_issued') + item_request.quantity
                        item_to_issue_obj.save(update_fields=['quantity_issued'])

                        StockTransaction.objects.create(
                            item=item_to_issue_obj,
                            transaction_type='Issue',
                            quantity=-item_request.quantity,
                            issued_to=item_request.requestor.username,
                            reason=f"Issued for request ID: {item_request.id} ({item_request.item.name})",
                            recorded_by=request.user
                        )
                        item_request.status = 'Issued'
                        item_request.processed_by = request.user
                        item_request.processed_at = timezone.now()
                        item_request.save()
                        messages.success(request, f'Request ID {item_request.id} ({item_request.item.name}) issued and marked as Issued.')
                    else:
                        messages.error(request, "Invalid request action.")

            except Exception as e:
                messages.error(request, f"Error processing request: {e}")

            return redirect('issue_item')

        # If it's not a request action, it must be the IssueItemForm submission
        form = IssueItemForm(request.POST)
        if form.is_valid():
            item_to_issue = form.cleaned_data['item']
            quantity = form.cleaned_data['quantity']
            issued_to = form.cleaned_data['issued_to']
            notes = form.cleaned_data['notes']

            try:
                with transaction.atomic():
                    if item_to_issue.quantity_remaining() < quantity:
                        messages.error(request, f"Not enough stock for {item_to_issue.name}. Available: {item_to_issue.quantity_remaining()}.")
                        context = {
                            'form': form,
                            'all_requests': all_requests,
                            'pending_and_approved_requests': pending_and_approved_requests,
                        }
                        return render(request, 'invent/issue_item.html', context)

                    item_to_issue.quantity_issued = F('quantity_issued') + quantity
                    item_to_issue.save(update_fields=['quantity_issued'])

                    StockTransaction.objects.create(
                        item=item_to_issue,
                        transaction_type='Issue',
                        quantity=-quantity,
                        issued_to=issued_to,
                        reason=f"Direct issue to {issued_to}. " + notes,
                        recorded_by=request.user
                    )
                messages.success(request, f'{quantity} x {item_to_issue.name} successfully issued to {issued_to}.')
                return redirect('issue_item')
            except Exception as e:
                messages.error(request, f"Error issuing item: {e}")
        else:
            messages.error(request, "Please correct the errors below for the issue form.")

    context = {
        'form': form,
        'all_requests': all_requests,
        'pending_and_approved_requests': pending_and_approved_requests,
        'approved_requests': all_requests.filter(status='Approved'),
        'issued_requests': all_requests.filter(status='Issued'),
        'rejected_requests': all_requests.filter(status='Rejected'),
        'pending_requests': all_requests.filter(status='Pending'),
    }
    return render(request, 'invent/issue_item.html', context)


@login_required
def search_items(request):
    query = request.GET.get('q')
    results = InventoryItem.objects.none()

    if query:
        results = InventoryItem.objects.filter(
            name__icontains=query
        ).order_by('name')

    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'invent/search_items.html', context)


@login_required
def request_summary(request):
    # Filter all requests to only those made by the logged-in requestor
    user_requests = ItemRequest.objects.filter(requestor=request.user)

    total_requests = user_requests.count()
    pending_requests = user_requests.filter(status='Pending').count()
    approved_requests = user_requests.filter(status='Approved').count()
    issued_requests = user_requests.filter(status='Issued').count()
    rejected_requests = user_requests.filter(status='Rejected').count()

    requests_by_status = user_requests.values('status').annotate(count=Count('id')).order_by('status')

    requests_by_item = user_requests.values('item__name').annotate(count=Sum('quantity')).order_by('-count')[:10]

    # No need to show top requestors to the current requestor (omit or just show current user’s total)
    # Alternatively, show how many times *they* requested:
    requests_by_requestor = user_requests.values('requestor__username').annotate(count=Count('id'))

    context = {
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
        'issued_requests': issued_requests,
        'rejected_requests': rejected_requests,
        'requests_by_status': requests_by_status,
        'requests_by_item': requests_by_item,
        'requests_by_requestor': requests_by_requestor,
    }
    return render(request, 'invent/request_summary.html', context)

@login_required
@permission_required('invent.change_inventoryitem', raise_exception=True)
def adjust_stock(request):
    if request.method == 'POST':
        form = AdjustStockForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data['item']
            adjustment_quantity = form.cleaned_data['adjustment_quantity']
            reason = form.cleaned_data['reason']
            notes = form.cleaned_data['notes']

            try:
                with transaction.atomic():
                    item.quantity_total = F('quantity_total') + adjustment_quantity
                    item.save(update_fields=['quantity_total'])

                    transaction_type = 'Add' if adjustment_quantity > 0 else 'Remove'

                    StockTransaction.objects.create(
                        item=item,
                        transaction_type=transaction_type,
                        quantity=adjustment_quantity,
                        reason=reason,
                        notes=notes,
                        recorded_by=request.user
                    )
                messages.success(request, f'Stock for {item.name} adjusted by {adjustment_quantity}. New total: {item.quantity_total}.')
                return redirect('adjust_stock')
            except Exception as e:
                messages.error(request, f"Error adjusting stock: {e}")
        else:
            messages.error(request, "Please correct the errors in the adjustment form.")
    else:
        form = AdjustStockForm()

    recent_transactions = StockTransaction.objects.filter(transaction_type__in=['Add', 'Remove']).order_by('-transaction_date')[:10]

    context = {
        'form': form,
        'recent_transactions': recent_transactions,
    }
    return render(request, 'invent/adjust_stock.html', context)