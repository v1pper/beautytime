from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from .models import Service, Master, Booking
from django.views.decorators.csrf import csrf_exempt
import json

def booking_page(request):
    return render(request, 'index.html')

def service_list(request):
    services = Service.objects.filter(is_active=True)
    data = []
    for service in services:
        data.append({
            'id': service.id,
            'name': service.name,
            'price': str(service.price),
            'duration': str(service.duration),
            'description': service.description,
            'category': service.category,
            'image': service.get_image(),
            'is_active': service.is_active
        })
    return JsonResponse(data, safe=False)

def master_list(request):
    masters = Master.objects.filter(is_active=True).select_related('user').prefetch_related('services')
    data = []
    for master in masters:
        data.append({
            'id': master.id,
            'user': {
                'first_name': master.user.first_name,
                'last_name': master.user.last_name
            },
            'specialization': master.get_specialization_display(),
            'specialization_code': master.specialization,
            'photo': master.get_photo(),
            'experience': master.experience,
            'rating': float(master.rating),
            'description': master.description,
            'instagram': master.instagram,
            'phone': master.phone,
            'services': [service.id for service in master.services.all()]
        })
    return JsonResponse(data, safe=False)

def master_detail(request, master_id):
    try:
        master = Master.objects.get(id=master_id, is_active=True)
        data = {
            'id': master.id,
            'user': {
                'first_name': master.user.first_name,
                'last_name': master.user.last_name
            },
            'specialization': master.get_specialization_display(),
            'photo': master.get_photo(),
            'experience': master.experience,
            'rating': float(master.rating),
            'description': master.description,
            'instagram': master.instagram,
            'phone': master.phone,
            'services': []
        }
        
        for service in master.services.filter(is_active=True):
            data['services'].append({
                'id': service.id,
                'name': service.name,
                'price': str(service.price),
                'duration': str(service.duration),
                'description': service.description,
                'image': service.get_image()
            })
            
        return JsonResponse(data)
    except Master.DoesNotExist:
        return JsonResponse({'error': 'Мастер не найден'}, status=404)

@csrf_exempt
def create_booking(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            existing_booking = Booking.objects.filter(
                master_id=data['master'],
                date=data['date'],
                time=data['time'],
                status__in=['pending', 'confirmed']
            ).exists()
            
            if existing_booking:
                return JsonResponse({'error': 'Это время уже занято'}, status=400)
            
            booking = Booking.objects.create(
                client_name=data['client_name'],
                client_email=data['client_email'],
                client_phone=data['client_phone'],
                service_id=data['service'],
                master_id=data['master'],
                date=data['date'],
                time=data['time']
            )
            return JsonResponse({
                'id': booking.id,
                'status': 'success',
                'message': 'Бронирование создано успешно'
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)