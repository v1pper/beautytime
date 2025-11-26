from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, RegexValidator, MinValueValidator, MaxValueValidator, URLValidator
from django.urls import reverse

class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название услуги")
    description = models.TextField(verbose_name="Описание", blank=True)
    duration = models.DurationField(verbose_name="Продолжительность")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    category = models.CharField(max_length=100, verbose_name="Категория", default="Общая")
    image = models.ImageField(upload_to='services/', blank=True, null=True, verbose_name="Изображение")
    image_url = models.URLField(
        max_length=500, 
        blank=True, 
        null=True, 
        verbose_name="Ссылка на изображение",
        validators=[URLValidator()],
        help_text="Можно указать ссылку на изображение из интернета"
    )
    
    def __str__(self):
        return self.name
    
    def get_image(self):
        """Возвращает изображение - сначала из файла, потом по ссылке"""
        if self.image:
            return self.image.url
        elif self.image_url:
            return self.image_url
        return None
    
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ['name']

class Master(models.Model):
    SPECIALIZATION_CHOICES = [
        ('hair', '💇 Парикмахер'),
        ('nails', '💅 Ногтевой сервис'),
        ('cosmetology', '✨ Косметология'),
        ('massage', '💆 Массаж'),
        ('eyebrows', '✏️ Брови и ресницы'),
        ('makeup', '💄 Визаж'),
    ]
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="Пользователь",
        related_name='master_profile'
    )
    specialization = models.CharField(
        max_length=50, 
        choices=SPECIALIZATION_CHOICES, 
        verbose_name="Специализация"
    )
    photo = models.ImageField(
        upload_to='masters/photos/', 
        blank=True, 
        null=True, 
        verbose_name="Фото мастера",
        help_text="Рекомендуемый размер: 400x400px"
    )
    photo_url = models.URLField(
        max_length=500, 
        blank=True, 
        null=True, 
        verbose_name="Ссылка на фото",
        validators=[URLValidator()],
        help_text="Можно указать ссылку на фото из интернета"
    )
    experience = models.PositiveIntegerField(
        default=0, 
        verbose_name="Опыт работы (лет)",
        validators=[MaxValueValidator(50)]
    )
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        default=5.0, 
        verbose_name="Рейтинг",
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    description = models.TextField(
        verbose_name="Описание мастера", 
        blank=True,
        help_text="Краткое описание опыта и специализации"
    )
    services = models.ManyToManyField(
        Service, 
        verbose_name="Услуги", 
        related_name='masters',
        blank=True
    )
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    display_order = models.PositiveIntegerField(
        default=0, 
        verbose_name="Порядок отображения",
        help_text="Чем меньше число, тем выше в списке"
    )
    instagram = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="Instagram",
        help_text="Имя пользователя без @"
    )
    phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(regex=r'^[\+]?[0-9]{10,15}$')],
        verbose_name="Телефон мастера",
        blank=True
    )
    work_schedule = models.JSONField(
        default=dict,
        verbose_name="График работы",
        help_text="JSON с графиком работы",
        blank=True,
        null=True
    )
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_specialization_display()}"
    
    def get_photo(self):
        """Возвращает фото - сначала из файла, потом по ссылке"""
        if self.photo:
            return self.photo.url
        elif self.photo_url:
            return self.photo_url
        return None
    
    def get_absolute_url(self):
        return reverse('admin:booking_master_change', args=[self.id])
    
    def get_full_name(self):
        return self.user.get_full_name()
    
    get_full_name.short_description = "Полное имя"
    
    def get_services_count(self):
        return self.services.count()
    
    get_services_count.short_description = "Кол-во услуг"
    
    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"
        ordering = ['display_order', 'user__first_name']

class MasterSchedule(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Понедельник'),
        (1, 'Вторник'),
        (2, 'Среда'),
        (3, 'Четверг'),
        (4, 'Пятница'),
        (5, 'Суббота'),
        (6, 'Воскресенье'),
    ]
    
    master = models.ForeignKey(
        Master, 
        on_delete=models.CASCADE, 
        verbose_name="Мастер",
        related_name='schedules'
    )
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK, verbose_name="День недели")
    start_time = models.TimeField(verbose_name="Время начала")
    end_time = models.TimeField(verbose_name="Время окончания")
    is_working = models.BooleanField(default=True, verbose_name="Рабочий день")
    
    class Meta:
        verbose_name = "График работы мастера"
        verbose_name_plural = "Графики работы мастеров"
        unique_together = ['master', 'day_of_week']
        ordering = ['master', 'day_of_week']

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', '⏳ Ожидает подтверждения'),
        ('confirmed', '✅ Подтверждена'),
        ('completed', '🎉 Выполнена'),
        ('cancelled', '❌ Отменена'),
    ]
    
    client_name = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2)],
        verbose_name="Имя клиента"
    )
    client_email = models.EmailField(verbose_name="Email клиента")
    client_phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(regex=r'^[\+]?[0-9]{10,15}$')],
        verbose_name="Телефон клиента"
    )
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Услуга")
    master = models.ForeignKey(Master, on_delete=models.CASCADE, verbose_name="Мастер")
    date = models.DateField(verbose_name="Дата")
    time = models.TimeField(verbose_name="Время")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        verbose_name="Статус"
    )
    notes = models.TextField(verbose_name="Примечания", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлена")
    
    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        unique_together = ['master', 'date', 'time']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.client_name} - {self.service} - {self.date} {self.time}"