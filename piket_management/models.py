"""
Models for piket_management app - PeriodePiket & JadwalPiket
"""
from django.db import models
from accounts.models import Users
import uuid


class KepengurusanLab(models.Model):
    """Kepengurusan Lab model from SILAB database"""
    id = models.CharField(max_length=36, primary_key=True)
    tahun_kepengurusan_id = models.CharField(max_length=36)
    laboratorium_id = models.CharField(max_length=36)
    sk = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'kepengurusan_lab'
        managed = False

    def __str__(self):
        return f"{self.id}"
    
    def get_display_name(self):
        """Get display name for dropdown"""
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT l.nama, t.tahun
                    FROM kepengurusan_lab kl
                    LEFT JOIN laboratorium l ON kl.laboratorium_id = l.id
                    LEFT JOIN tahun_kepengurusan t ON kl.tahun_kepengurusan_id = t.id
                    WHERE kl.id = %s
                """, [self.id])
                row = cursor.fetchone()
                if row:
                    lab_nama, tahun = row
                    return f"{lab_nama} - {tahun} - {self.sk or 'No SK'}"
        except:
            pass
        return self.id


class PeriodePiket(models.Model):
    """Periode Piket model from SILAB database"""
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False)
    kepengurusan_lab_id = models.CharField(max_length=36)
    nama = models.CharField(max_length=255)
    tanggal_mulai = models.DateField()
    tanggal_selesai = models.DateField()
    isactive = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'periode_piket'
        managed = False

    def __str__(self):
        return self.nama


class JadwalPiket(models.Model):
    """Jadwal Piket model from SILAB database"""
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False)
    hari = models.CharField(max_length=255)
    kepengurusan_lab_id = models.CharField(max_length=36)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'jadwal_piket'
        managed = False

    def __str__(self):
        return f"{self.user.name} - {self.hari}"
