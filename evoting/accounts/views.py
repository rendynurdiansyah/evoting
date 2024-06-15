from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from evoting.views import *
from dashboard.views import *

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Ganti dengan URL dashboard admin Anda
        else:
            return render(request, 'accounts/login-admin.html', {'error': 'Invalid credentials'})
    return render(request, 'accounts/login-admin.html')

@login_required
def admin_logout(request):
    logout(request)
    return redirect('admin_login')


def admin_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        
        if password == password_confirm:
            if User.objects.filter(username=username).exists():
                return render(request, 'accounts/register-admin.html', {'error': 'Username already exists'})
            else:
                user = User.objects.create_user(username=username, password=password)
                user.is_staff = True
                user.save()
                login(request, user)
                return redirect('dashboard')  # Ganti dengan URL dashboard admin Anda
        else:
            return render(request, 'accounts/register-admin.html', {'error': 'Passwords do not match'})
    return render(request, 'accounts/register-admin.html')

def pemilih_login(request):
    if request.method == 'POST':
        nim = request.POST.get('nim')
        pemilih = get_object_or_404(Pemilih, nim=nim)
        request.session['pemilih_id'] = pemilih.id
        return redirect('voting')
    return render(request, 'accounts/login.html')

def pemilih_logout(request):
    logout(request)
    return redirect('pemilih_login')