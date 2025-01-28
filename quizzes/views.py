# quizzes/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import QuestionOption, Quiz, QuizAttempt, Question, UserResponse
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
        total_questions = quiz.questions.count()
        correct_answers = 0
        user_responses = []  # Store responses temporarily

        # Loop through the questions and validate user responses
        for question in quiz.questions.all():
            answer = request.POST.get(f"question_{question.id}")
            is_correct = False
            selected_option = None
            short_answer_text = None

            if answer:
                if question.question_type == 'SA':
                    # Handle Short Answer questions
                    correct_option = question.options.filter(is_correct=True).first()
                    if correct_option and answer.lower().strip() == correct_option.text.lower().strip():
                        score += 1
                        is_correct = True
                        correct_answers += 1
                    short_answer_text = answer

                elif question.question_type == 'TF':
                    # Handle True/False questions
                    if answer == 'True':
                        if question.options.filter(text='True', is_correct=True).exists():
                            score += 1
                            is_correct = True
                            correct_answers += 1
                    elif answer == 'False':
                        if question.options.filter(text='False', is_correct=True).exists():
                            score += 1
                            is_correct = True
                            correct_answers += 1
                    selected_option = question.options.filter(text=answer).first()

                else:  # Multiple Choice questions
                    try:
                        selected_option = QuestionOption.objects.get(id=int(answer))
                        if selected_option.is_correct:
                            score += 1
                            is_correct = True
                            correct_answers += 1
                    except (ValueError, QuestionOption.DoesNotExist):
                        continue

            # Store response data
            user_responses.append({
                'question': question,
                'selected_option': selected_option,
                'short_answer_text': short_answer_text,
                'is_correct': is_correct
            })

        # Calculate percentage score
        percentage_score = (score / total_questions) * 100 if total_questions > 0 else 0

        # Create quiz attempt record
        quiz_attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=percentage_score,
            total_questions=total_questions,
            correct_answers=correct_answers
        )

        # Create all UserResponse objects after QuizAttempt is created
        for response in user_responses:
            UserResponse.objects.create(
                attempt=quiz_attempt,
                question=response['question'],
                selected_option=response['selected_option'],
                short_answer_text=response['short_answer_text'],
                is_correct=response['is_correct']
            )

        return redirect('quiz_results', quiz_id=quiz.id)

    return render(request, 'quiz_attempt.html', {'quiz': quiz})
