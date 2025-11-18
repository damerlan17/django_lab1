from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    # Добавим поле для "времени жизни" в днях
    expiration_days = models.PositiveIntegerField(default=30)
    # Добавим поле для краткого описания (по ТЗ)
    short_description = models.CharField(max_length=200, blank=True)
    # Добавим поле для изображения (по ТЗ)
    image = models.ImageField(upload_to='poll_images/', blank=True, null=True)

    def __str__(self):
        return self.question_text

    def is_expired(self):
        """Возвращает True, если опрос истек."""
        expiration_date = self.pub_date + timedelta(days=self.expiration_days)
        return timezone.now() > expiration_date

    @property
    def full_description(self):
        """Свойство для полного описания (пока совпадает с вопросом)."""
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class Vote(models.Model):
    """Модель для отслеживания голосов пользователей."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    vote_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question')