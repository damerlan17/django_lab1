# polls/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Question, Choice, Vote

def index(request):
    # Получаем все вопросы, дата публикации которых уже наступила
    potential_active_questions = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')

    # Фильтруем на стороне Python, оставляя только те, которые не истекли
    active_questions = []
    for question in potential_active_questions:
        if not question.is_expired(): # Используем метод модели is_expired
            active_questions.append(question)

    # Берем первые 5 активных вопросов
    latest_question_list = active_questions[:5]

    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if question.is_expired():
        messages.info(request, "Этот опрос больше не активен.")
    return render(request, 'polls/detail.html', {'question': question})

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if question.is_expired():
        messages.error(request, "Голосование за этот вопрос завершено.")
        return redirect('polls:detail', question_id=question.id)

    try:
        selected_choice = question.choices.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Показываем форму с ошибкой.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Вы не выбрали вариант.",
        })
    else:
        # Проверяем, голосовал ли пользователь за этот вопрос
        try:
            existing_vote = Vote.objects.get(user=request.user, question=question)
            # Если голос уже есть, обновляем его
            existing_vote.choice.votes -= 1 # Уменьшаем голос старого выбора
            existing_vote.choice.save()
            existing_vote.choice = selected_choice # Меняем выбор
            existing_vote.choice.votes += 1 # Увеличиваем голос нового выбора
            existing_vote.choice.save()
            existing_vote.save()
            messages.success(request, "Ваш голос был обновлен.")
        except Vote.DoesNotExist:
            # Если голоса нет, создаем новый
            selected_choice.votes += 1
            selected_choice.save()
            Vote.objects.create(user=request.user, question=question, choice=selected_choice)
            messages.success(request, "Спасибо за ваш голос!")

        return redirect('polls:results', question_id=question.id)

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    total_votes = sum([choice.votes for choice in question.choices.all()])
    context = {
        'question': question,
        'total_votes': total_votes,
    }
    return render(request, 'polls/results.html', context)