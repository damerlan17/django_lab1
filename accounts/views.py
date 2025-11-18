from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        profile_form = ProfileUpdateForm(request.POST, request.FILES) # Для загрузки аватара
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            # Связываем профиль с пользователем
            profile = user.profile # Используем related_name из модели
            profile.avatar = profile_form.cleaned_data.get('avatar')
            profile.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} создан! Теперь вы можете войти.')
            return redirect('login') # Перенаправляем на страницу входа
    else:
        form = UserRegisterForm()
        profile_form = ProfileUpdateForm()

    return render(request, 'accounts/register.html', {'form': form, 'profile_form': profile_form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile) # instance=request.user.profile

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Ваш профиль обновлён!')
            return redirect('profile') # Перенаправляем обратно на страницу профиля, чтобы избежать повторной отправки формы

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile) # instance=request.user.profile

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'accounts/profile.html', context=context)

@login_required
def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, f'Ваш профиль был удалён.')
        return redirect('posts:index') # Или на другую страницу после удаления

    return render(request, 'accounts/profile_confirm_delete.html')

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Ваш профиль обновлён!')
            # --- ИЗМЕНЕНИЕ ТУТ ---
            return redirect('accounts:profile') # Используй namespace 'accounts'
            # --- /ИЗМЕНЕНИЕ ---
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'accounts/profile.html', context=context)