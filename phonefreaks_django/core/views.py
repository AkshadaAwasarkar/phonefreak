import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Phone, Wishlist, Comparison, Review

def index(request):
    phones = Phone.objects.all()
    return render(request, 'index.html', {'phones': phones})

def phone_detail(request, phone_id):
    phone = get_object_or_404(Phone, id=phone_id)
    return render(request, 'phone_detail.html', {'phone': phone})

def compare(request):
    phones = Phone.objects.all()
    phones_dict = {
        phone.id: {
            'brand': phone.brand,
            'model': phone.model,
            'image': phone.image,
            'prices': phone.prices,
            'specs': phone.specs
        } for phone in phones
    }
    phones_json = json.dumps(phones_dict)
    return render(request, 'compare.html', {'phones': phones, 'phones_json': phones_json})

@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AdminLoginForm, PhoneForm
from .decorators import admin_required
from django.contrib.auth.models import User
from .models import UserProfile

def admin_login_view(request):
    if request.user.is_authenticated and hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'admin':
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        form = AdminLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if hasattr(user, 'userprofile') and user.userprofile.role == 'admin':
                login(request, user)
                return redirect('admin_dashboard')
            elif user.is_staff or user.is_superuser: # Fallback for superusers/staff without profile setup yet
                 login(request, user)
                 return redirect('admin_dashboard')
            else:
                messages.error(request, "Access denied. Admin privileges required.")
    else:
        form = AdminLoginForm()
    return render(request, 'admin_login.html', {'form': form})

@admin_required
def admin_dashboard(request):
    phones = Phone.objects.all().order_by('-id')
    return render(request, 'admin_dashboard.html', {'phones': phones})

@admin_required
def admin_add_phone(request):
    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Phone added successfully!")
            return redirect('admin_dashboard')
    else:
        form = PhoneForm()
    return render(request, 'admin_phone_form.html', {'form': form, 'title': 'Add New Phone'})

@admin_required
def admin_edit_phone(request, phone_id):
    phone = get_object_or_404(Phone, id=phone_id)
    if request.method == 'POST':
        form = PhoneForm(request.POST, instance=phone)
        if form.is_valid():
            form.save()
            messages.success(request, "Phone updated successfully!")
            return redirect('admin_dashboard')
    else:
        form = PhoneForm(instance=phone)
    return render(request, 'admin_phone_form.html', {'form': form, 'title': f'Edit {phone.model}'})

@admin_required
def admin_delete_phone(request, phone_id):
    if request.method == 'POST':
        phone = get_object_or_404(Phone, id=phone_id)
        phone.delete()
        messages.success(request, "Phone deleted successfully!")
    return redirect('admin_dashboard')

@admin_required
def manage_users(request):
    users = User.objects.all().select_related('userprofile')
    return render(request, 'manage_users.html', {'users': users})

@admin_required
def toggle_admin_role(request, user_id):
    user_to_toggle = get_object_or_404(User, id=user_id)
    # Prevent modifying own role
    if user_to_toggle == request.user:
        messages.error(request, "You cannot change your own role.")
        return redirect('manage_users')

    if not hasattr(user_to_toggle, 'userprofile'):
        UserProfile.objects.create(user=user_to_toggle)
    
    profile = user_to_toggle.userprofile
    if profile.role == 'admin':
        profile.role = 'user'
        messages.success(request, f"Revoked admin access for {user_to_toggle.username}")
    else:
        profile.role = 'admin'
        messages.success(request, f"Granted admin access to {user_to_toggle.username}")
    profile.save()
    
    return redirect('manage_users')
