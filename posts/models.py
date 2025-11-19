# posts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone # Убедись, что импортирован
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=200)
    short_description = models.CharField(max_length=300)
    full_description = models.TextField(null=True, blank=True) # Предполагается, что это новый или переименованный атрибут
    pub_date = models.DateTimeField(default=timezone.now)
    # --- Изменение в поле ---
    expiration_time = models.DateTimeField(default=timezone.now) # Или любое другое значение по умолчанию
    # Например, через 30 дней:
    # expiration_time = models.DateTimeField(default=lambda: timezone.now() + timezone.timedelta(days=30))
    # --- /Изменение ---
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    @property
    def expiration_days(self):
        """Возвращает количество дней до окончания действия поста."""
        if self.is_expired():
            return 0  # Или отрицательное число, если просрочен
        time_diff = self.expiration_time - timezone.now()
        return time_diff.days

    def __str__(self):
        return self.title

    def is_expired(self):
        return timezone.now() > self.expiration_time

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'pk': self.pk})

