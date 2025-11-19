from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'short_description', 'full_description', 'expiration_time', 'image'] # Укажи нужные поля
        # widgets = {
        #     'expiration_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}), # Улучшенный вид для даты/времени
        # }