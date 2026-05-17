from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

# ===========================
# SIGN UP VIEW
# ===========================
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        # Validasi input
        if not username or not password or not confirm:
            messages.error(request, "Semua field wajib diisi.")
            return redirect('signup')

        if password != confirm:
            messages.error(request, "Password tidak cocok.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username sudah digunakan.")
            return redirect('signup')

        # Buat akun baru
        User.objects.create_user(username=username, password=password)
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect('login')

    return render(request, 'FlatKit/signup.html')


# ===========================
# LOGIN VIEW
# ===========================
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Selamat datang, {username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Username atau password salah.")

    return render(request, 'FlatKit/signin.html')


# ===========================
# LOGOUT VIEW
# ===========================
def logout_view(request):
    logout(request)
    messages.info(request, "Anda telah logout.")
    return redirect('login')


# ===========================
# DASHBOARD VIEW
# ===========================
@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'FlatKit/dashboard.0.html')
