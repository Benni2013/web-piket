"""
Models for accounts app - Using SILAB database tables
"""
from django.db import models
import uuid


class Users(models.Model):
    """User model from SILAB database"""
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    password = models.CharField(max_length=255)
    laboratory_id = models.CharField(max_length=36, null=True, blank=True)
    remember_token = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        managed = False  # Django won't manage this table

    def __str__(self):
        return self.name


class Profile(models.Model):
    """Profile model from SILAB database"""
    JENIS_KELAMIN_CHOICES = [
        ('laki-laki', 'Laki-laki'),
        ('perempuan', 'Perempuan'),
    ]
    
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False)
    nomor_induk = models.CharField(max_length=255)
    jenis_kelamin = models.CharField(max_length=20, choices=JENIS_KELAMIN_CHOICES)
    foto_profile = models.CharField(max_length=255, null=True, blank=True)
    alamat = models.CharField(max_length=255, null=True, blank=True)
    no_hp = models.CharField(max_length=255, null=True, blank=True)
    tempat_lahir = models.CharField(max_length=255, null=True, blank=True)
    tanggal_lahir = models.DateField(null=True, blank=True)
    nomor_anggota = models.CharField(max_length=255, null=True, blank=True)
    user = models.OneToOneField(Users, on_delete=models.CASCADE, db_column='user_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'profile'
        managed = False  # Django won't manage this table

    def __str__(self):
        return f"Profile of {self.user.name}"
