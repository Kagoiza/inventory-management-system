
from django.shortcuts import render, redirect
from django.contrib.auth.forms import  AuthenticationForm
from .forms import CustomCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ItemRequest, InventoryItem, Item
from .forms import ManageStockForm

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
    return redirect('login')


@login_required
def requestor_dashboard(request):
    user_requests = ItemRequest.objects.filter(requestor=request.user)

    # Count status totals
    total_requests = user_requests.count()
    approved_count = user_requests.filter(status='Approved').count()
    pending_count = user_requests.filter(status='Pending').count()

    return render(request, 'invent/requestor_dashboard.html', {
        'requests': user_requests,
        'total_requests': total_requests,
        'approved_count': approved_count,
        'pending_count': pending_count,
    })

from .forms import RequestItemForm

@login_required
def request_item(request):
    if request.method == 'POST':
        form = RequestItemForm(request.POST)
        if form.is_valid():
            item_request = form.save(commit=False)
            item_request.requestor = request.user
            item_request.save()
            return redirect('requestor_dashboard')
    else:
        form = RequestItemForm()
    return render(request, 'invent/request_item.html', {'form': form})


@login_required
def store_clerk_dashboard(request):
    items = InventoryItem.objects.all()

    context = {
        'items': items,
        'total_items': items.count(),
        'items_issued': sum(item.quantity_issued for item in items),
        'items_returned': sum(item.quantity_returned for item in items),
    }
    return render(request, 'invent/store_clerk_dashboard.html', context)


@login_required
def manage_stock(request):
    if request.method == 'POST':
        form = ManageStockForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock item added or updated successfully.')
            return redirect('manage_stock')
    else:
        form = ManageStockForm()

    items = Item.objects.all()
    return render(request, 'invent/manage_stock.html', {'form': form, 'items': items})

