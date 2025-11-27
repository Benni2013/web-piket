from django.urls import path
from . import views

app_name = 'piket_management'

urlpatterns = [
    # Periode Piket
    path('periode/', views.periode_list, name='periode_list'),
    path('periode/create/', views.periode_create, name='periode_create'),
    path('periode/<str:id>/update/', views.periode_update, name='periode_update'),
    path('periode/<str:id>/delete/', views.periode_delete, name='periode_delete'),
    path('periode/<str:id>/activate/', views.periode_activate, name='periode_activate'),
    
    # Jadwal Piket
    path('jadwal/', views.jadwal_list, name='jadwal_list'),
    path('jadwal/create/', views.jadwal_create, name='jadwal_create'),
    path('jadwal/<str:id>/update/', views.jadwal_update, name='jadwal_update'),
    path('jadwal/<str:id>/delete/', views.jadwal_delete, name='jadwal_delete'),
]
