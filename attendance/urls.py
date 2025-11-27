from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('mulai/', views.mulai_piket, name='mulai_piket'),
    path('akhiri/', views.akhiri_piket, name='akhiri_piket'),
    path('report/', views.report_absensi, name='report_absensi'),
]
