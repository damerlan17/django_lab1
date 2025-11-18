from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Post

def index(request):
    # Получаем все посты, дата публикации которых уже наступила
    potential_active_posts = Post.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')

    # Фильтруем на стороне Python, оставляя только те, которые не истекли
    active_posts = []
    for post in potential_active_posts:
        if not post.is_expired(): # Используем метод модели is_expired
            active_posts.append(post)

    # Берем первые 5 активных постов
    latest_post_list = active_posts[:5]

    context = {'latest_post_list': latest_post_list}
    return render(request, 'posts/index.html', context)

def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    # Проверяем, истек ли пост, и выводим сообщение
    if post.is_expired():
        messages.info(request, "Этот пост больше не активен.")
    return render(request, 'posts/detail.html', {'post': post})