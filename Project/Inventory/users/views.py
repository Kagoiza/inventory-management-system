from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout # Import necessary auth functions
from django.contrib.auth.decorators import login_required # For protecting the home page
from django.contrib.auth.forms import AuthenticationForm # Django's built-in login form
from .forms import CustomUserCreationForm # Your custom registration form

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
            user = form.save() # Save the new user to the database
            auth_login(request, user) # Log the user in immediately
            messages.success(request, f'Account created for {user.username}!')
            return redirect('home') # Redirect to the home page
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
        # Use Django's built-in AuthenticationForm
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user) # Log the user in
                messages.info(request, f'You are now logged in as {username}.')
                return redirect('home') # Redirect to the home page
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
    return redirect('login') # Redirect to the login page after logout

# --- Basic Homepage View (Protected) ---
@login_required # This decorator ensures only logged-in users can access this page
def home(request):
    """
    A basic homepage view that requires the user to be logged in.
    """
    return render(request, 'users/home.html')
