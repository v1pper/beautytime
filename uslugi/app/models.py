from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, RegexValidator

class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название услуги")
    description = models.TextField(verbose_name="Описание", blank=True)
    duration = models.DurationField(verbose_name="Продолжительность")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

class Master(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    specialization = models.CharField(max_length=200, verbose_name="Специализация")
    photo = models.ImageField(upload_to='masters/', blank=True, null=True, verbose_name="Фото")
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"

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
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")
    
    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        unique_together = ['master', 'date', 'time']
    
    def __str__(self):
        return f"{self.client_name} - {self.service} - {self.date} {self.time}"