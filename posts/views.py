from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required # Обычно создание постов доступно только авторизованным
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.views.generic import ListView, DetailView # Добавь ListView и DetailView
from .models import Post
from .forms import PostForm



@login_required # Только для авторизованных пользователей
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES) # request.FILES для загрузки изображений
        if form.is_valid():
            post = form.save(commit=False) # Пока не сохраняем в БД
            post.author = request.user # Устанавливаем автора
            post.save() # Теперь сохраняем
            messages.success(request, f'Пост "{post.title}" создан!')
            return redirect('posts:detail', pk=post.pk) # Перенаправляем на страницу созданного поста
    else:
        form = PostForm()

    return render(request, 'posts/create_post.html', {'form': form})
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

# Класс для отображения списка постов
class PostListView(ListView):
    model = Post
    template_name = 'posts/index.html'  # Укажи путь к шаблону
    context_object_name = 'latest_post_list'


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/detail.html' # Укажи путь к шаблону
    context_object_name = 'post'