from django.urls import path
from . import views

app_name = 'accounts' # Важно для namespace

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/delete/', views.delete_profile, name='delete_profile'),
    path('profile/logout/', views.user_logout, name='logout'),
    # Можно добавить и другие URL, например, для просмотра чужого профиля
]
