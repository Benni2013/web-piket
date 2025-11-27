"""
Models for attendance app - Absensi
"""
from django.db import models
from accounts.models import Users
from piket_management.models import JadwalPiket, PeriodePiket
import uuid


class Absensi(models.Model):
    """Absensi model from SILAB database"""
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False)
    tanggal = models.DateField()
    jam_masuk = models.TimeField()
    jam_keluar = models.TimeField(null=True, blank=True)
    foto = models.CharField(max_length=255)
    jadwal_piket = models.CharField(max_length=36)
    kegiatan = models.TextField()
    periode_piket_id = models.CharField(max_length=36)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'absensi'
        managed = False

    def __str__(self):
        return f"Absensi - {self.tanggal}"
    
    def get_user(self):
        """Get user from jadwal_piket"""
        try:
            jp = JadwalPiket.objects.get(id=self.jadwal_piket)
            return jp.user
        except JadwalPiket.DoesNotExist:
            return None
    
    def get_periode(self):
        """Get periode piket"""
        try:
            return PeriodePiket.objects.get(id=self.periode_piket_id)
        except PeriodePiket.DoesNotExist:
            return None
    
    @property
    def durasi(self):
        """Calculate duration in hours and minutes"""
        if self.jam_masuk and self.jam_keluar:
            from datetime import datetime, timedelta
            masuk = datetime.combine(self.tanggal, self.jam_masuk)
            keluar = datetime.combine(self.tanggal, self.jam_keluar)
            delta = keluar - masuk
            
            hours = delta.seconds // 3600
            minutes = (delta.seconds % 3600) // 60
            
            return f"{hours} jam {minutes} menit"
        return "-"
