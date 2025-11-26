from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking_page, name='booking'),
    path('api/services/', views.service_list, name='service-list'),
    path('api/masters/', views.master_list, name='master-list'),
    path('api/masters/<int:master_id>/', views.master_detail, name='master-detail'),
    path('api/bookings/', views.create_booking, name='create-booking'),
]