"""
Views for attendance app - Mulai/Akhiri Piket & Report
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Q
from .models import Absensi
from accounts.models import Users, Profile
from piket_management.models import PeriodePiket
import requests
import json
from datetime import date


def dashboard(request):
    """Dashboard - show today's attendance status"""
    if not request.session.get('user_id'):
        return redirect('accounts:login')
    
    user = Users.objects.get(id=request.session['user_id'])
    today = date.today()
    
    # Check if user has started piket today
    # Get user's jadwal_piket first
    from piket_management.models import JadwalPiket
    user_jadwal_ids = JadwalPiket.objects.filter(user=user).values_list('id', flat=True)
    
    absensi_today = Absensi.objects.filter(
        jadwal_piket__in=user_jadwal_ids,
        tanggal=today
    ).first()
    
    # Get active periode
    active_periode = PeriodePiket.objects.filter(isactive=True).first()
    
    context = {
        'user': user,
        'absensi_today': absensi_today,
        'active_periode': active_periode,
        'today': today,
    }
    return render(request, 'attendance/dashboard.html', context)


def mulai_piket(request):
    """Start piket with face recognition"""
    if not request.session.get('user_id'):
        return redirect('accounts:login')
    
    if request.method == 'POST':
        try:
            # Get image from POST data (JSON)
            data = json.loads(request.body)
            image = data.get('image')
            
            if not image:
                return JsonResponse({'success': False, 'message': 'No image provided'})
            
            # Call API Piket - Mulai Piket
            api_url = f"{settings.API_PIKET_URL}/api/piket/mulai"
            payload = {
                'image': image
            }
            
            response = requests.post(api_url, json=payload)
            result = response.json()
            
            if result.get('success'):
                # Check if recognized user matches logged-in user
                recognized_user_id = result['data']['user_id']
                if recognized_user_id == request.session['user_id']:
                    messages.success(request, f"Piket dimulai! Selamat bertugas.")
                    return JsonResponse({'success': True, 'redirect': '/'})
                else:
                    return JsonResponse({
                        'success': False, 
                        'message': 'Wajah yang terdeteksi tidak sesuai dengan user yang login!'
                    })
            else:
                return JsonResponse({
                    'success': False, 
                    'message': result.get('message', 'Face not recognized')
                })
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return render(request, 'attendance/mulai_piket.html')


def akhiri_piket(request):
    """End piket with face verification"""
    if not request.session.get('user_id'):
        return redirect('accounts:login')
    
    # Check if user has started piket today
    user = Users.objects.get(id=request.session['user_id'])
    today = date.today()
    
    # Get user's jadwal_piket first
    from piket_management.models import JadwalPiket
    user_jadwal_ids = JadwalPiket.objects.filter(user=user).values_list('id', flat=True)
    
    absensi_today = Absensi.objects.filter(
        jadwal_piket__in=user_jadwal_ids,
        tanggal=today,
        jam_masuk__isnull=False
    ).first()
    
    if not absensi_today:
        messages.error(request, 'Anda belum mulai piket hari ini!')
        return redirect('attendance:dashboard')
    
    if absensi_today.jam_keluar:
        messages.warning(request, 'Anda sudah mengakhiri piket hari ini!')
        return redirect('attendance:dashboard')
    
    if request.method == 'POST':
        try:
            # Get image and kegiatan from POST data (JSON)
            data = json.loads(request.body)
            image = data.get('image')
            kegiatan = data.get('kegiatan')
            
            if not image or not kegiatan:
                return JsonResponse({'success': False, 'message': 'Image dan kegiatan harus diisi'})
            
            # Call API Piket - Akhiri Piket
            api_url = f"{settings.API_PIKET_URL}/api/piket/akhiri"
            payload = {
                'image': image,
                'kegiatan': kegiatan
            }
            
            response = requests.post(api_url, json=payload)
            result = response.json()
            
            if result.get('success'):
                # Check if recognized user matches logged-in user
                recognized_user_id = result['data']['user_id']
                if recognized_user_id == request.session['user_id']:
                    messages.success(request, f"Piket selesai! Durasi: {result['data']['durasi']}")
                    return JsonResponse({'success': True, 'redirect': '/'})
                else:
                    return JsonResponse({
                        'success': False, 
                        'message': 'Wajah yang terdeteksi tidak sesuai dengan user yang login!'
                    })
            else:
                return JsonResponse({
                    'success': False, 
                    'message': result.get('message', 'Face not recognized')
                })
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return render(request, 'attendance/akhiri_piket.html')


def report_absensi(request):
    """Report absensi piket"""
    if not request.session.get('user_id'):
        return redirect('accounts:login')
    
    # Get filter parameters
    periode_id = request.GET.get('periode_id')
    user_id = request.GET.get('user_id')
    
    # Base query - Note: jadwal_piket and periode_piket_id are CharField, not ForeignKey
    absensis = Absensi.objects.all()
    
    # Apply filters
    if periode_id:
        absensis = absensis.filter(periode_piket_id=periode_id)
    
    if user_id:
        # Filter by user through jadwal_piket
        from piket_management.models import JadwalPiket
        jadwal_ids = JadwalPiket.objects.filter(user_id=user_id).values_list('id', flat=True)
        absensis = absensis.filter(jadwal_piket__in=jadwal_ids)
    
    # Order by date descending
    absensis = absensis.order_by('-tanggal', '-jam_masuk')
    
    # Get all periodes and users for filter dropdown
    periodes = PeriodePiket.objects.all().order_by('-created_at')
    users = Users.objects.all().order_by('name')
    
    context = {
        'absensis': absensis,
        'periodes': periodes,
        'users': users,
        'selected_periode': periode_id,
        'selected_user': user_id,
    }
    return render(request, 'attendance/report_absensi.html', context)
