# quizzes/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import QuestionOption, Quiz, QuizAttempt, Question
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
    return render(request, 'quiz_detail.html', {
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


@login_required
def subject_selection(request):
    return render(request, 'subject_selection.html')

@login_required
def subject_quizzes(request, subject):
    quizzes = Quiz.objects.filter(subject__iexact=subject)
    return render(request, 'subject_quizzes.html', {
        'subject': subject,
        'quizzes': quizzes
    })

@login_required
def mathematics_quiz(request):
    return render(request, 'mathematics.html')

@login_required
def science_quiz(request):
    return render(request, 'science.html')

@login_required
def english_quiz(request):
    return render(request, 'english.html')


def quiz_attempt(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        score = 0
        # Loop through the questions and validate user responses
        for question in quiz.questions.all():
            selected_option_id = request.POST.get(f"question_{question.id}")

            if selected_option_id:
                try:
                    if question.question_type == 'TF':  # Handling True/False
                        # Directly check for 'True' or 'False'
                        if selected_option_id == 'True':
                            # Check if the question is correct
                            if question.options.filter(text='True', is_correct=True).exists():
                                score += 1
                        elif selected_option_id == 'False':
                            # Check if the question is correct
                            if question.options.filter(text='False', is_correct=True).exists():
                                score += 1
                    else:
                        # Handle MC or SA questions as before
                        selected_option = QuestionOption.objects.get(id=selected_option_id)
                        if selected_option.is_correct:
                            score += 1
                except QuestionOption.DoesNotExist:
                    # Handle the case where the selected option is invalid
                    continue

        # Create a quiz attempt record
        quiz_attempt = QuizAttempt.objects.create(user=request.user, quiz=quiz, score=score)
        return redirect('quiz_results', quiz_id=quiz.id)  # Redirect to result or summary page

    return render(request, 'quiz_attempt.html', {'quiz': quiz})
