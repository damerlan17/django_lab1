# monolith_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    path('posts/', include('posts.urls')),
    # path('accounts/', include('accounts.urls')), # Возможно, ты убрал это или поменял местами
    path('accounts/', include('django.contrib.auth.urls')), # Подключено под 'accounts/'
    path('my_accounts/', include('accounts.urls')), # А свои URL под 'my_accounts/'
]

# Обязательно для отображения загруженных файлов (включая аватары) в режиме отладки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)