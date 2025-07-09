# C:\Users\Bumi\OneDrive\Documents\Projects\inventory-management-system\Project\Inventory\invent\views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Sum, F # <-- IMPORTANT: Added F for atomic updates
from django.db import transaction # <-- IMPORTANT: Added transaction for atomic operations

# Correct Model and Form Imports
from .models import ItemRequest, InventoryItem, Item, StockTransaction # <-- IMPORTANT: Added StockTransaction
from .forms import ItemRequestForm
from .forms import InventoryItemForm
from .forms import IssueItemForm, AdjustStockForm # <-- IMPORTANT: Added new forms
from django.db.models import Q


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
    user_requests = ItemRequest.objects.filter(requestor=request.user)

    total_requests = user_requests.count()
    approved_count = user_requests.filter(status='Approved').count()
    pending_count = user_requests.filter(status='Pending').count()

    return render(request, 'invent/requestor_dashboard.html', {
        'requests': user_requests,
        'total_requests': total_requests,
        'approved_count': approved_count,
        'pending_count': pending_count,
    })

# --- Request Item Funcntionality

@login_required
def request_item(request):
    item_id = request.GET.get('item_id')
    item = get_object_or_404(Item, id=item_id)

    if request.method == 'POST':
        form = ItemRequestForm(request.POST)
        if form.is_valid():
            request_obj = form.save(commit=False)

            request_obj.item = item
            request_obj.requestor = request.user  # ✅ Make sure this line is present

            print("DEBUG - User making request:", request.user)
            print("DEBUG - Requestor set as:", request_obj.requestor)

            if item.quantity >= request_obj.quantity:
                request_obj.status = "Pending"
                request_obj.save()
                messages.success(request, "Your request has been submitted successfully.")
                return redirect('requestor_dashboard')
            else:
                messages.warning(request, "Not enough stock available. Please reduce the quantity.")
        else:
            print("DEBUG - Form errors:", form.errors)
    else:
        form = ItemRequestForm()

    return render(request, 'invent/request_item.html', {
        'form': form,
        'item': item
    })

# --- Request Summary ---
@login_required
def request_summary(request):
    requests = ItemRequest.objects.filter(requestor=request.user).order_by('-date_requested')
    return render(request, 'invent/request_summary.html', {'requests': requests})

# --- Cancel Request ---

@login_required
def cancel_request(request, request_id):
    item_request = get_object_or_404(ItemRequest, id=request_id, requestor=request.user)

    if item_request.status == 'Pending':
        item_request.status = 'Cancelled'
        item_request.save()

        # Optionally restore stock
        item_request.item.quantity += item_request.quantity
        item_request.item.save()

        messages.success(request, "Your request was cancelled and stock restored.")
    else:
        messages.warning(request, "You can only cancel pending requests.")

    return redirect('request_summary')  # or 'my_requests'


# --- Store Clerk Functionality ---

@login_required
@permission_required('invent.view_inventoryitem', raise_exception=True)
def store_clerk_dashboard(request):
    inventory_items = InventoryItem.objects.all()
    
    # Calculate totals from InventoryItem instances
    # Use sum on the `quantity_total` field across all inventory items
    total_inventory_items = inventory_items.aggregate(total_sum=Sum('quantity_total'))['total_sum'] or 0
    items_issued = inventory_items.aggregate(total_issued=Sum('quantity_issued'))['total_issued'] or 0
    items_returned = inventory_items.aggregate(total_returned=Sum('quantity_returned'))['total_returned'] or 0

    items_for_dashboard = inventory_items.order_by('-created_at')[:5]

    context = {
        'total_items': total_inventory_items, # Renamed variable for clarity
        'items_issued': items_issued,
        'items_returned': items_returned,
        'items': items_for_dashboard,
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


# --- FULLY IMPLEMENTED VIEWS for Issue Item and Adjust Stock ---

@login_required
@permission_required('invent.can_issue_item', raise_exception=True) # Using custom permission 'can_issue_item'
def issue_item(request):
    if request.method == 'POST':
        form = IssueItemForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data['item']
            quantity = form.cleaned_data['quantity']
            issued_to = form.cleaned_data['issued_to']
            notes = form.cleaned_data['notes']

            try:
                with transaction.atomic(): # Ensures all updates succeed or fail together
                    # Update InventoryItem quantities atomically
                    # quantity_issued increases
                    item.quantity_issued = F('quantity_issued') + quantity
                    # quantity_total should not change here if it represents all items ever physically received.
                    # It changes only for adjustments/receipts.
                    # The `quantity_remaining` property on the model calculates available stock.
                    item.save(update_fields=['quantity_issued'])

                    # Create a StockTransaction record
                    StockTransaction.objects.create(
                        item=item,
                        transaction_type='Issue',
                        quantity=-quantity, # Negative to denote items removed from available stock
                        issued_to=issued_to,
                        reason=f"Issued to {issued_to}. " + notes, # Combine notes with recipient for reason
                        recorded_by=request.user
                    )
                messages.success(request, f'{quantity} x {item.name} successfully issued to {issued_to}.')
                return redirect('store_clerk_dashboard') # Redirect after successful operation
            except Exception as e:
                messages.error(request, f"Error issuing item: {e}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = IssueItemForm()

    context = {
        'form': form,
    }
    return render(request, 'invent/issue_item.html', context)


@login_required
@permission_required('invent.can_adjust_stock', raise_exception=True) # Using custom permission 'can_adjust_stock'
def adjust_stock(request):
    if request.method == 'POST':
        form = AdjustStockForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data['item']
            adjustment_quantity = form.cleaned_data['adjustment_quantity']
            reason = form.cleaned_data['reason']
            notes = form.cleaned_data['notes']

            try:
                with transaction.atomic(): # Ensures all updates succeed or fail together
                    # Update InventoryItem total quantity atomically
                    item.quantity_total = F('quantity_total') + adjustment_quantity
                    # Ensure quantity_total doesn't become negative after adjustment
                    if (item.quantity_total + adjustment_quantity) < 0: # This check is redundant with form validation, but good for safety
                         raise ValueError("Adjustment would result in negative total stock.")
                    item.save(update_fields=['quantity_total'])

                    # Create a StockTransaction record
                    StockTransaction.objects.create(
                        item=item,
                        transaction_type='Adjustment',
                        quantity=adjustment_quantity, # Quantity can be positive or negative
                        reason=reason,
                        notes=notes, # Store notes separately if you want, or combine with reason
                        recorded_by=request.user
                    )
                
                action_msg = "added to" if adjustment_quantity > 0 else "removed from"
                messages.success(request, f'{abs(adjustment_quantity)} x {item.name} {action_msg} stock. Reason: {reason}.')
                return redirect('store_clerk_dashboard') # Redirect after successful operation
            except Exception as e:
                messages.error(request, f"Error adjusting stock: {e}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AdjustStockForm()

    context = {
        'form': form,
    }
    return render(request, 'invent/adjust_stock.html', context)

# --- Search Items Functionality

@login_required
def search_items(request):
    query = request.GET.get('q', '')
    condition_filter = request.GET.get('condition', '')

    items = Item.objects.all()

    if query:
        items = items.filter(
            Q(name__icontains=query) |
            Q(category__icontains=query) |
            Q(department__icontains=query)
        )

    if condition_filter:
        items = items.filter(condition=condition_filter)

    context = {
        'items': items,
        'query': query,
        'condition_filter': condition_filter
    }
    return render(request, 'invent/search_items.html', context)