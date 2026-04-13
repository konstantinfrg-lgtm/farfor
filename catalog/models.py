from django.db import models
from django.contrib.auth.models import User


class Manufacturer(models.Model):
    """Производитель фарфора"""
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Sculptor(models.Model):
    """Скульптор"""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Скульптор'
        verbose_name_plural = 'Скульпторы'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Artist(models.Model):
    """Художник по росписи"""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Художник'
        verbose_name_plural = 'Художники'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Form(models.Model):
    """Название формы молочника"""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Форма'
        verbose_name_plural = 'Формы'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Painting(models.Model):
    """Название росписи"""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Роспись'
        verbose_name_plural = 'Росписи'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class MilkJug(models.Model):
    """Карточка молочника в коллекции"""
    
    VISIBILITY_CHOICES = [
        ('public', 'Публичный'),
        ('registered', 'Только для зарегистрированных'),
        ('private', 'Приватный'),
    ]
    
    CONDITION_CHOICES = [
        ('excellent', 'Отличное'),
        ('good', 'Хорошее'),
        ('satisfactory', 'Удовлетворительное'),
        ('poor', 'Плохое'),
        ('damaged', 'Поврежден'),
    ]
    
    # Основные поля
    manufacturer = models.ForeignKey(
        Manufacturer, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='milk_jugs',
        verbose_name='Производитель'
    )
    sculptor = models.ForeignKey(
        Sculptor, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='milk_jugs',
        verbose_name='Скульптор'
    )
    artist = models.ForeignKey(
        Artist, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='milk_jugs',
        verbose_name='Художник'
    )
    form = models.ForeignKey(
        Form, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='milk_jugs',
        verbose_name='Форма'
    )
    painting = models.ForeignKey(
        Painting, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='milk_jugs',
        verbose_name='Роспись'
    )
    
    # Дополнительные поля
    name = models.CharField(max_length=255, blank=True, verbose_name='Название предмета')
    year = models.CharField(max_length=50, blank=True, verbose_name='Год создания / период')
    material = models.CharField(max_length=100, blank=True, verbose_name='Материал')
    country = models.CharField(max_length=100, blank=True, verbose_name='Страна')
    factory = models.CharField(max_length=255, blank=True, verbose_name='Завод / фабрика')
    height = models.DecimalField(max_digits=6, decimal_places=1, blank=True, null=True, verbose_name='Высота (см)')
    volume = models.DecimalField(max_digits=6, decimal_places=1, blank=True, null=True, verbose_name='Объем (мл)')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, blank=True, verbose_name='Состояние')
    has_mark = models.BooleanField(default=False, verbose_name='Наличие клейма')
    mark_description = models.TextField(blank=True, verbose_name='Описание клейма')
    source = models.CharField(max_length=255, blank=True, verbose_name='Источник поступления')
    comments = models.TextField(blank=True, verbose_name='Комментарии')
    
    # Владелец и видимость
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='milk_jugs',
        verbose_name='Владелец'
    )
    visibility = models.CharField(
        max_length=20, 
        choices=VISIBILITY_CHOICES, 
        default='private',
        verbose_name='Видимость'
    )
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    
    # Даты
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Молочник'
        verbose_name_plural = 'Молочники'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['manufacturer', 'form', 'painting']),
            models.Index(fields=['owner', 'visibility']),
        ]
    
    def __str__(self):
        name_parts = []
        if self.manufacturer:
            name_parts.append(str(self.manufacturer))
        if self.form:
            name_parts.append(str(self.form))
        if self.painting:
            name_parts.append(str(self.painting))
        return ' / '.join(name_parts) if name_parts else f'Молочник #{self.id}'


class Photo(models.Model):
    """Фотография молочника"""
    milk_jug = models.ForeignKey(
        MilkJug, 
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name='Молочник'
    )
    image = models.ImageField(upload_to='milk_jugs/%Y/%m/%d/', verbose_name='Изображение')
    is_main = models.BooleanField(default=False, verbose_name='Главное фото')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')
    
    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
        ordering = ['order', '-is_main', 'uploaded_at']
    
    def __str__(self):
        return f'Фото для {self.milk_jug}'
    
    def save(self, *args, **kwargs):
        # Если фото главное, убираем главенство у других фото этого молочника
        if self.is_main:
            Photo.objects.filter(milk_jug=self.milk_jug, is_main=True).update(is_main=False)
        super().save(*args, **kwargs)
