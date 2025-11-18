
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static # Импортируем

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    path('posts/', include('posts.urls')),
    # Добавьте маршрут для главной страницы, если нужно
    # path('', include('polls.urls')), # например, если polls - главная
]

# Добавляем маршрут для медиафайлов в режиме отладки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)