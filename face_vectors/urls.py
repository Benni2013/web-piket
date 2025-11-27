from django.urls import path
from . import views

app_name = 'face_vectors'

urlpatterns = [
    path('insert/', views.insert_face, name='insert'),
    path('insert/camera/', views.insert_face_camera, name='insert_camera'),
    path('insert/upload/', views.insert_face_upload, name='insert_upload'),
    path('update/', views.update_face, name='update'),
    path('update/camera/', views.update_face_camera, name='update_camera'),
]
