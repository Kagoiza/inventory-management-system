from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm # Your custom registration form
from django.db import IntegrityError # Import IntegrityError

# --- Registration View ---
def register(request):
    """
    Handles user registration.
    - On GET: Displays an empty registration form.
    - On POST: Processes form data, creates a user, logs them in, redirects.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save() # Save the new user to the database
                auth_login(request, user) # Log the user in immediately
                messages.success(request, f'Account created for {user.username}!')
                return redirect('users:home') # <--- CHANGED HERE: Use namespaced URL
            except IntegrityError:
                messages.error(request, 'This username is already taken. Please choose a different one.')
                return render(request, 'users/register.html', {'form': form})
            except Exception as e:
                messages.error(request, f'An unexpected error occurred: {e}. Please try again.')
                return render(request, 'users/register.html', {'form': form})
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = CustomUserCreationForm() # Empty form for GET request
    return render(request, 'users/register.html', {'form': form})

# --- Login View (Customized for your template) ---
def login_view(request):
    """
    Handles user login.
    - On GET: Displays the login form.
    - On POST: Authenticates user, logs them in, redirects to home on success.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password) # Pass request to authenticate
            if user is not None:
                auth_login(request, user) # Log the user in
                messages.info(request, f'You are now logged in as {username}.')
                return redirect('users:home') # <--- CRITICAL CHANGE: Use namespaced URL
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm() # Empty form for GET request
    return render(request, 'users/login.html', {'form': form})

# --- Logout View ---
@login_required # Ensures only logged-in users can access this view
def logout_view(request):
    """
    Logs out the current user and redirects to the login page.
    """
    auth_logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('users:login_view') # <--- CHANGED HERE: Use namespaced URL

# --- Basic Homepage View (Protected) ---
@login_required # This decorator ensures only logged-in users can access this page
def home(request):
    """
    A basic homepage view that requires the user to be logged in.
    """
    return render(request, 'users/home.html')
