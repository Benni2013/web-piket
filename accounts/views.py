"""
Views for accounts app - Register, Login, Profile
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Users, Profile
import uuid


def register(request):
    """Register new user"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        nomor_induk = request.POST.get('nomor_induk')
        jenis_kelamin = request.POST.get('jenis_kelamin')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # Validation
        if not all([name, email, nomor_induk, jenis_kelamin, password, password_confirm]):
            messages.error(request, 'Semua field harus diisi!')
            return render(request, 'accounts/register.html')
        
        if password != password_confirm:
            messages.error(request, 'Password tidak cocok!')
            return render(request, 'accounts/register.html')
        
        if Users.objects.filter(email=email).exists():
            messages.error(request, 'Email sudah terdaftar!')
            return render(request, 'accounts/register.html')
        
        try:
            # Create user
            user = Users.objects.create(
                id=str(uuid.uuid4()),
                name=name,
                email=email,
                password=make_password(password)
            )
            
            # Create profile
            Profile.objects.create(
                id=str(uuid.uuid4()),
                user=user,
                nomor_induk=nomor_induk,
                jenis_kelamin=jenis_kelamin
            )
            
            messages.success(request, 'Registrasi berhasil! Silakan login.')
            return redirect('accounts:login')
            
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return render(request, 'accounts/register.html')
    
    return render(request, 'accounts/register.html')


def login_view(request):
    """Login user"""
    if request.session.get('user_id'):
        return redirect('attendance:dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password:
            messages.error(request, 'Email dan password harus diisi!')
            return render(request, 'accounts/login.html')
        
        try:
            user = Users.objects.get(email=email)
            
            if check_password(password, user.password):
                # Set session
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                request.session['user_email'] = user.email
                
                messages.success(request, f'Selamat datang, {user.name}!')
                return redirect('attendance:dashboard')
            else:
                messages.error(request, 'Email atau password salah!')
                
        except Users.DoesNotExist:
            messages.error(request, 'Email atau password salah!')
    
    return render(request, 'accounts/login.html')


def logout_view(request):
    """Logout user"""
    request.session.flush()
    messages.success(request, 'Anda telah logout.')
    return redirect('accounts:login')


def profile(request):
    """View user profile"""
    if not request.session.get('user_id'):
        return redirect('accounts:login')
    
    user = Users.objects.get(id=request.session['user_id'])
    
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
    
    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'accounts/profile.html', context)


def update_profile(request):
    """Update user profile"""
    if not request.session.get('user_id'):
        return redirect('accounts:login')
    
    if request.method == 'POST':
        user = Users.objects.get(id=request.session['user_id'])
        
        name = request.POST.get('name')
        nomor_induk = request.POST.get('nomor_induk')
        jenis_kelamin = request.POST.get('jenis_kelamin')
        alamat = request.POST.get('alamat', '')
        no_hp = request.POST.get('no_hp', '')
        tempat_lahir = request.POST.get('tempat_lahir', '')
        tanggal_lahir = request.POST.get('tanggal_lahir')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        
        try:
            # Update name
            if name:
                user.name = name
                request.session['user_name'] = name
            
            # Update password if provided
            if current_password and new_password:
                if check_password(current_password, user.password):
                    user.password = make_password(new_password)
                else:
                    messages.error(request, 'Password lama salah!')
                    return redirect('accounts:profile')
            
            user.save()
            
            # Update or create profile
            profile, created = Profile.objects.get_or_create(
                user=user,
                defaults={
                    'id': str(uuid.uuid4()), 
                    'nomor_induk': nomor_induk,
                    'jenis_kelamin': jenis_kelamin
                }
            )
            if not created:
                profile.nomor_induk = nomor_induk
                profile.jenis_kelamin = jenis_kelamin
                profile.alamat = alamat
                profile.no_hp = no_hp
                profile.tempat_lahir = tempat_lahir
                if tanggal_lahir:
                    profile.tanggal_lahir = tanggal_lahir
                profile.save()
            
            messages.success(request, 'Profile berhasil diupdate!')
            
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return redirect('accounts:profile')
