# quizzes/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, QuizAttempt, Question
from .forms import QuizCreationForm, QuizAttemptForm
from django.db.models import Avg

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes})

@login_required
def quiz_create(request):
    if request.method == 'POST':
        form = QuizCreationForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.created_by = request.user
            quiz.save()
            return redirect('quiz_detail', quiz_id=quiz.id)
    else:
        form = QuizCreationForm()
    return render(request, 'quiz_create.html', {'form': form})

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    avg_score = QuizAttempt.objects.filter(quiz=quiz).aggregate(Avg('score'))
    return render(request, 'quizzes/quiz_detail.html', {
        'quiz': quiz,
        'avg_score': avg_score['score__avg']
    })

@login_required
def quiz_attempt(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        form = QuizAttemptForm(request.POST, quiz=quiz)
        if form.is_valid():
            score = form.calculate_score()
            QuizAttempt.objects.create(
                user=request.user, 
                quiz=quiz, 
                score=score
            )
            return redirect('quiz_results', quiz_id=quiz.id)
    else:
        form = QuizAttemptForm(quiz=quiz)
    return render(request, 'quiz_attempt.html', {'form': form, 'quiz': quiz})

def quiz_results(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    attempt = QuizAttempt.objects.filter(
        user=request.user, 
        quiz=quiz
    ).latest('attempted_at')
    return render(request, 'quiz_results.html', {
        'quiz': quiz,
        'attempt': attempt
    })


def landing(request):
    return render(request, 'landing.html')