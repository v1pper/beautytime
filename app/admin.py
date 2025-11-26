from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import Service, Master, MasterSchedule, Booking

class MasterScheduleInline(admin.TabularInline):
    model = MasterSchedule
    extra = 7
    max_num = 7
    fields = ['day_of_week', 'start_time', 'end_time', 'is_working']
    ordering = ['day_of_week']

class ServicesInline(admin.TabularInline):
    model = Master.services.through
    extra = 1
    verbose_name = "Услуга мастера"
    verbose_name_plural = "Услуги мастера"

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = [
        'photo_preview',
        'get_full_name', 
        'specialization_display', 
        'experience',
        'rating',
        'get_services_count',
        'is_active',
        'display_order'
    ]
    list_display_links = ['photo_preview', 'get_full_name']
    list_filter = ['specialization', 'is_active', 'experience']
    list_editable = ['display_order', 'is_active', 'rating']
    search_fields = ['first_name', 'last_name', 'specialization']
    readonly_fields = ['photo_preview_large', 'photo_url_preview']
    filter_horizontal = ['services']
    inlines = [MasterScheduleInline, ServicesInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': (
                'first_name',
                'last_name',
                'specialization', 
                'experience',
                'rating',
                'description',
                'is_active',
                'display_order'
            )
        }),
        ('Контактная информация', {
            'fields': (
                'phone',
                'instagram',
            ),
            'classes': ('collapse',)
        }),
        ('Фотография (загрузка файла)', {
            'fields': (
                'photo',
                'photo_preview_large'
            )
        }),
        ('Фотография (ссылка из интернета)', {
            'fields': (
                'photo_url',
                'photo_url_preview'
            ),
            'classes': ('collapse',)
        }),
        ('График работы', {
            'fields': ('work_schedule',),
            'classes': ('collapse',)
        }),
    )
    
    def specialization_display(self, obj):
        return obj.get_specialization_display()
    specialization_display.short_description = 'Специализация'
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()
    get_full_name.short_description = 'Полное имя'
    
    def photo_preview(self, obj):
        photo_url = obj.get_photo()
        if photo_url:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 50%;" />',
                photo_url
            )
        return "📷"
    photo_preview.short_description = 'Фото'
    
    def photo_preview_large(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="width: 200px; height: 200px; object-fit: cover; border-radius: 10px;" />',
                obj.photo.url
            )
        return "Фото не загружено"
    photo_preview_large.short_description = 'Предпросмотр загруженного фото'
    photo_preview_large.allow_tags = True
    
    def photo_url_preview(self, obj):
        if obj.photo_url:
            return format_html(
                '''
                <div>
                    <img src="{}" style="width: 200px; height: 200px; object-fit: cover; border-radius: 10px; margin-bottom: 10px;" />
                    <div><strong>Ссылка:</strong> <a href="{}" target="_blank">{}</a></div>
                </div>
                ''',
                obj.photo_url, obj.photo_url, obj.photo_url
            )
        return "Ссылка на фото не указана"
    photo_url_preview.short_description = 'Предпросмотр фото по ссылке'
    photo_url_preview.allow_tags = True
    
    def get_services_count(self, obj):
        return obj.services.count()
    get_services_count.short_description = 'Кол-во услуг'
    
    def get_queryset(self, request):
        return super().get_queryset(request)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = [
        'image_preview',
        'name', 
        'category', 
        'price', 
        'duration', 
        'is_active'
    ]
    list_display_links = ['image_preview', 'name']
    list_filter = ['category', 'is_active']
    list_editable = ['price', 'is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['image_preview_large', 'image_url_preview']
    
    fieldsets = (
        ('Основная информация', {
            'fields': (
                'name',
                'description',
                'category',
                'price',
                'duration',
                'is_active'
            )
        }),
        ('Изображение (загрузка файла)', {
            'fields': (
                'image',
                'image_preview_large'
            )
        }),
        ('Изображение (ссылка из интернета)', {
            'fields': (
                'image_url',
                'image_url_preview'
            )
        }),
    )
    
    def image_preview(self, obj):
        image_url = obj.get_image()
        if image_url:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 8px;" />',
                image_url
            )
        return "🖼️"
    image_preview.short_description = 'Изобр.'
    
    def image_preview_large(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 200px; height: 200px; object-fit: cover; border-radius: 10px;" />',
                obj.image.url
            )
        return "Изображение не загружено"
    image_preview_large.short_description = 'Предпросмотр загруженного изображения'
    image_preview_large.allow_tags = True
    
    def image_url_preview(self, obj):
        if obj.image_url:
            return format_html(
                '''
                <div>
                    <img src="{}" style="width: 200px; height: 200px; object-fit: cover; border-radius: 10px; margin-bottom: 10px;" />
                    <div><strong>Ссылка:</strong> <a href="{}" target="_blank">{}</a></div>
                </div>
                ''',
                obj.image_url, obj.image_url, obj.image_url
            )
        return "Ссылка на изображение не указана"
    image_url_preview.short_description = 'Предпросмотр изображения по ссылке'
    image_url_preview.allow_tags = True

@admin.register(MasterSchedule)
class MasterScheduleAdmin(admin.ModelAdmin):
    list_display = ['master', 'day_of_week', 'start_time', 'end_time', 'is_working']
    list_filter = ['day_of_week', 'is_working', 'master']
    list_editable = ['start_time', 'end_time', 'is_working']
    ordering = ['master', 'day_of_week']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'client_name', 
        'service', 
        'master', 
        'date', 
        'time', 
        'status',
        'created_at'
    ]
    list_filter = ['status', 'date', 'master', 'service']
    search_fields = ['client_name', 'client_email', 'client_phone']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'

# Убираем связь с User так как у нас теперь отдельная модель Master
# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)