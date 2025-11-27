"""
Views for face_vectors app - Insert & Update face vectors
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import requests
import json
import base64


def insert_face(request):
    """Choose method for inserting face vectors"""
    if not request.session.get('user_id'):
        return redirect('accounts:login')
    
    return render(request, 'face_vectors/insert.html')


def insert_face_camera(request):
    """Insert face vectors using camera (20 photos)"""
    if not request.session.get('user_id'):
        return redirect('accounts:login')
    
    if request.method == 'POST':
        try:
            # Get images from POST data (JSON)
            data = json.loads(request.body)
            images = data.get('images', [])
            
            if not images:
                return JsonResponse({'success': False, 'message': 'No images provided'})
            
            # Call API Piket
            api_url = f"{settings.API_PIKET_URL}/api/face/insert"
            payload = {
                'user_id': request.session['user_id'],
                'images': images
            }
            
            response = requests.post(api_url, json=payload)
            result = response.json()
            
            if result.get('success'):
                messages.success(request, f"Berhasil menyimpan {result['data']['embeddings_saved']} vektor wajah!")
                return JsonResponse({'success': True, 'redirect': '/face/insert/'})
            else:
                return JsonResponse({'success': False, 'message': result.get('message', 'Error')})
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return render(request, 'face_vectors/insert_camera.html')


def insert_face_upload(request):
    """Insert face vector from uploaded photo"""
    if not request.session.get('user_id'):
        return redirect('accounts:login')
    
    if request.method == 'POST':
        try:
            photo = request.FILES.get('photo')
            
            if not photo:
                messages.error(request, 'Pilih foto terlebih dahulu!')
                return redirect('face_vectors:insert_upload')
            
            # Convert to base64
            photo_data = photo.read()
            photo_base64 = f"data:image/jpeg;base64,{base64.b64encode(photo_data).decode('utf-8')}"
            
            # Call API Piket
            api_url = f"{settings.API_PIKET_URL}/api/face/insert-from-photo"
            payload = {
                'user_id': request.session['user_id'],
                'image': photo_base64
            }
            
            response = requests.post(api_url, json=payload)
            result = response.json()
            
            if result.get('success'):
                messages.success(request, 'Vektor wajah berhasil disimpan!')
            else:
                messages.error(request, result.get('message', 'Gagal menyimpan vektor wajah'))
                
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'face_vectors/insert_upload.html')


def update_face(request):
    """Choose method for updating face vectors"""
    if not request.session.get('user_id'):
        return redirect('accounts:login')
    
    return render(request, 'face_vectors/update.html')


def update_face_camera(request):
    """Update face vectors using camera (20 photos)"""
    if not request.session.get('user_id'):
        return redirect('accounts:login')
    
    if request.method == 'POST':
        try:
            # Get images from POST data (JSON)
            data = json.loads(request.body)
            images = data.get('images', [])
            
            if not images:
                return JsonResponse({'success': False, 'message': 'No images provided'})
            
            # Call API Piket
            api_url = f"{settings.API_PIKET_URL}/api/face/update/{request.session['user_id']}"
            payload = {
                'images': images
            }
            
            response = requests.put(api_url, json=payload)
            result = response.json()
            
            if result.get('success'):
                messages.success(request, f"Berhasil update {result['data']['new_vectors_count']} vektor wajah!")
                return JsonResponse({'success': True, 'redirect': '/face/update/'})
            else:
                return JsonResponse({'success': False, 'message': result.get('message', 'Error')})
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return render(request, 'face_vectors/update_camera.html')


# Import JsonResponse
from django.http import JsonResponse
