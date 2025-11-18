from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class MediaItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField(max_length=500, verbose_name="URL")
    alt = models.CharField(max_length=255, blank=True, verbose_name="Альтернативный текст")
    width = models.IntegerField(null=True, blank=True, verbose_name="Ширина")
    height = models.IntegerField(null=True, blank=True, verbose_name="Высота")
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name="Медиафайл"
        verbose_name_plural="Медиафайлы"

    def __str__(self):
        return self.alt or self.url

class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    street = models.CharField(max_length=255, verbose_name="Улица")
    city = models.CharField(max_length=100, verbose_name="Город")
    postcode = models.CharField(max_length=20, verbose_name="Почтовый индекс")
    region = models.CharField(max_length=100, verbose_name="Регион")
    country = models.CharField(max_length=100, verbose_name="Страна")
    full = models.CharField(max_length=500, verbose_name="Полный адрес")

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"

class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)  
    specialty = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class Education(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    institution = models.CharField(max_length=255, verbose_name="Учебное заведение")
    degree = models.CharField(max_length=100, verbose_name="Степень")
    specialty = models.CharField(max_length=255, verbose_name="Специальность")
    year_graduated = models.IntegerField(verbose_name="Год окончания")
    certificate = models.TextField(blank=True, verbose_name="Сертификат")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Образование"
        verbose_name_plural = "Образование"

    def __str__(self):
        return f"{self.institution} - {self.specialty} ({self.year_graduated})"


class WorkingHours(models.Model):
    DAYS_OF_WEEK = [
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        'Organization',
        on_delete=models.CASCADE,
        related_name='working_hours',
    )
    day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK, verbose_name="День")
    opens_at = models.TimeField(verbose_name="Время открытия")
    closes_at = models.TimeField(verbose_name="Время закрытия")

    class Meta:
        verbose_name_plural = "Рабочие часы"
        unique_together = ['organization', 'day_of_week']

    def __str__(self):
        return f"{self.organization.name} - {self.get_day_of_week_display()} {self.opens_at}-{self.closes_at}"


class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='reviews')
    author_name = models.CharField(max_length=255)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Review by {self.author_name} for {self.doctor}'

class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name="Название")
    # эти поля опциональны — на скринах они используются для location
    location_lat = models.FloatField(null=True, blank=True)
    location_lng = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name="Название услуги")

    def __str__(self):
        return self.name
