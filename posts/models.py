# posts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Post(models.Model):
    title = models.CharField(max_length=50) # ТЗ: до 50 символов
    content = models.TextField() # ТЗ: неограниченная длина
    pub_date = models.DateTimeField('date published', auto_now_add=True) # Дата публикации
    expiration_days = models.PositiveIntegerField(default=30) # Время жизни
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # Автор (опционально или по ТЗ)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True) # Изображение к посту (по ТЗ)

    def __str__(self):
        return self.title

    def is_expired(self):
        """Возвращает True, если пост истек."""
        expiration_date = self.pub_date + timedelta(days=self.expiration_days)
        return timezone.now() > expiration_date
