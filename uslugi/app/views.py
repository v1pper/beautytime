from django.shortcuts import render
from django.http import JsonResponse
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
            'is_active': service.is_active
        })
    return JsonResponse(data, safe=False)

def master_list(request):
    masters = Master.objects.all()
    data = []
    for master in masters:
        data.append({
            'id': master.id,
            'user': {
                'first_name': master.user.first_name,
                'last_name': master.user.last_name
            },
            'specialization': master.specialization,
            'photo': master.photo.url if master.photo else None
        })
    return JsonResponse(data, safe=False)

@csrf_exempt
def create_booking(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
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
                'status': 'success'
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)