# posts/urls.py
from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:post_id>/', views.detail, name='detail'),
    path('', views.PostListView.as_view(), name='index'),  # или views.index, если используешь функцию
    path('<int:pk>/', views.PostDetailView.as_view(), name='detail'),  # или views.detail
    path('create/', views.create_post, name='create'),  # <-- Добавь этот URL
]