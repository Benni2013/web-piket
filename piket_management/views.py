"""
Views for piket_management app - CRUD Periode & Jadwal Piket
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import PeriodePiket, JadwalPiket, KepengurusanLab
from accounts.models import Users
import uuid


# ==================== PERIODE PIKET ====================

def periode_list(request):
    """List all periode piket"""
    if not request.session.get('user_id'):
        return redirect('accounts:login')
    
    periodes = PeriodePiket.objects.all().order_by('-created_at')
    
    context = {
        'periodes': periodes,
    }
    return render(request, 'piket_management/periode_list.html', context)


def periode_create(request):
    """Create new periode piket"""
    if not request.session.get('user_id'):
        return redirect('accounts:login')
    
    if request.method == 'POST':
        kepengurusan_lab_id = request.POST.get('kepengurusan_lab_id')
        nama = request.POST.get('nama')
        tanggal_mulai = request.POST.get('tanggal_mulai')
        tanggal_selesai = request.POST.get('tanggal_selesai')
        isactive = request.POST.get('isactive') == 'on'
        
        if not all([kepengurusan_lab_id, nama, tanggal_mulai, tanggal_selesai]):
            messages.error(request, 'Semua field harus diisi!')
            kepengurusan_labs = KepengurusanLab.objects.all()
            context = {'kepengurusan_labs': kepengurusan_labs}
            return render(request, 'piket_management/periode_form.html', context)
        
        try:
            # If set to active, deactivate all others
            if isactive:
                PeriodePiket.objects.all().update(isactive=False)
            
            PeriodePiket.objects.create(
                id=str(uuid.uuid4()),
                kepengurusan_lab_id=kepengurusan_lab_id,
                nama=nama,
                tanggal_mulai=tanggal_mulai,
                tanggal_selesai=tanggal_selesai,
                isactive=isactive
            )
            
            messages.success(request, 'Periode piket berhasil dibuat!')
            return redirect('piket_management:periode_list')
            
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    kepengurusan_labs = KepengurusanLab.objects.all()
    context = {'kepengurusan_labs': kepengurusan_labs}
    return render(request, 'piket_management/periode_form.html', context)


def periode_update(request, id):
    """Update periode piket"""
    if not request.session.get('user_id'):
        return redirect('accounts:login')
    
    periode = get_object_or_404(PeriodePiket, id=id)
    
    if request.method == 'POST':
        kepengurusan_lab_id = request.POST.get('kepengurusan_lab_id')
        nama = request.POST.get('nama')
        tanggal_mulai = request.POST.get('tanggal_mulai')
        tanggal_selesai = request.POST.get('tanggal_selesai')
        isactive = request.POST.get('isactive') == 'on'
        
        try:
            # If set to active, deactivate all others
            if isactive:
                PeriodePiket.objects.exclude(id=id).update(isactive=False)
            
            periode.kepengurusan_lab_id = kepengurusan_lab_id
            periode.nama = nama
            periode.tanggal_mulai = tanggal_mulai
            periode.tanggal_selesai = tanggal_selesai
            periode.isactive = isactive
            periode.save()
            
            messages.success(request, 'Periode piket berhasil diupdate!')
            return redirect('piket_management:periode_list')
            
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    kepengurusan_labs = KepengurusanLab.objects.all()
    context = {
        'periode': periode,
        'kepengurusan_labs': kepengurusan_labs,
    }
    return render(request, 'piket_management/periode_form.html', context)


def periode_delete(request, id):
    """Delete periode piket"""
    if not request.session.get('user_id'):
        return redirect('accounts:login')
    
    periode = get_object_or_404(PeriodePiket, id=id)
    
    try:
        periode.delete()
        messages.success(request, 'Periode piket berhasil dihapus!')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
    
    return redirect('piket_management:periode_list')


def periode_activate(request, id):
    """Activate periode piket (deactivate others)"""
    if not request.session.get('user_id'):
        return redirect('accounts:login')
    
    try:
        PeriodePiket.objects.all().update(isactive=False)
        periode = get_object_or_404(PeriodePiket, id=id)
        periode.isactive = True
        periode.save()
        
        messages.success(request, f'Periode "{periode.nama}" diaktifkan!')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
    
    return redirect('piket_management:periode_list')


# ==================== JADWAL PIKET ====================

def jadwal_list(request):
    """List all jadwal piket"""
    if not request.session.get('user_id'):
        return redirect('accounts:login')
    
    jadwals = JadwalPiket.objects.select_related('user').all().order_by('hari')
    
    context = {
        'jadwals': jadwals,
    }
    return render(request, 'piket_management/jadwal_list.html', context)


def jadwal_create(request):
    """Create new jadwal piket"""
    if not request.session.get('user_id'):
        return redirect('accounts:login')
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        hari = request.POST.get('hari')
        kepengurusan_lab_id = request.POST.get('kepengurusan_lab_id')
        
        if not all([user_id, hari, kepengurusan_lab_id]):
            messages.error(request, 'Semua field harus diisi!')
            users = Users.objects.all()
            kepengurusan_labs = KepengurusanLab.objects.all()
            context = {
                'users': users,
                'kepengurusan_labs': kepengurusan_labs,
            }
            return render(request, 'piket_management/jadwal_form.html', context)
        
        try:
            user = Users.objects.get(id=user_id)
            
            JadwalPiket.objects.create(
                id=str(uuid.uuid4()),
                hari=hari,
                kepengurusan_lab_id=kepengurusan_lab_id,
                user=user
            )
            
            messages.success(request, 'Jadwal piket berhasil dibuat!')
            return redirect('piket_management:jadwal_list')
            
        except Users.DoesNotExist:
            messages.error(request, 'User tidak ditemukan!')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    users = Users.objects.all()
    kepengurusan_labs = KepengurusanLab.objects.all()
    
    context = {
        'users': users,
        'kepengurusan_labs': kepengurusan_labs,
    }
    return render(request, 'piket_management/jadwal_form.html', context)


def jadwal_update(request, id):
    """Update jadwal piket"""
    if not request.session.get('user_id'):
        return redirect('accounts:login')
    
    jadwal = get_object_or_404(JadwalPiket, id=id)
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        hari = request.POST.get('hari')
        kepengurusan_lab_id = request.POST.get('kepengurusan_lab_id')
        
        try:
            user = Users.objects.get(id=user_id)
            
            jadwal.user = user
            jadwal.hari = hari
            jadwal.kepengurusan_lab_id = kepengurusan_lab_id
            jadwal.save()
            
            messages.success(request, 'Jadwal piket berhasil diupdate!')
            return redirect('piket_management:jadwal_list')
            
        except Users.DoesNotExist:
            messages.error(request, 'User tidak ditemukan!')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    users = Users.objects.all()
    kepengurusan_labs = KepengurusanLab.objects.all()
    
    context = {
        'jadwal': jadwal,
        'users': users,
        'kepengurusan_labs': kepengurusan_labs,
    }
    return render(request, 'piket_management/jadwal_form.html', context)


def jadwal_delete(request, id):
    """Delete jadwal piket"""
    if not request.session.get('user_id'):
        return redirect('accounts:login')
    
    jadwal = get_object_or_404(JadwalPiket, id=id)
    
    try:
        jadwal.delete()
        messages.success(request, 'Jadwal piket berhasil dihapus!')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
    
    return redirect('piket_management:jadwal_list')
