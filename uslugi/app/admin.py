from django.contrib import admin
from .models import Service, Master, Booking

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration', 'is_active']
    list_filter = ['is_active']

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'specialization']
    
    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_full_name.short_description = 'Мастер'

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'service', 'master', 'date', 'time', 'status']
    list_filter = ['status', 'date']