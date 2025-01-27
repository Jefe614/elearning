# quizzes/models.py
from django.db import models
from django.conf import settings

class Quiz(models.Model):
    QUESTION_TYPES = [
        ('MC', 'Multiple Choice'),
        ('TF', 'True/False'),
        ('SA', 'Short Answer')
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    grade_level = models.IntegerField()
    subject = models.CharField(max_length=100)    
    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    question_type = models.CharField(max_length=2, choices=Quiz.QUESTION_TYPES)
    image = models.ImageField(upload_to='question_images/', null=True, blank=True)
    
    def __str__(self):
        return self.text[:50]

class QuestionOption(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

class QuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField()
    total_questions = models.PositiveIntegerField(blank=True, null=True)
    correct_answers = models.PositiveIntegerField(blank=True, null=True)
    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} ({self.score})"


class UserResponse(models.Model):
    attempt = models.ForeignKey(QuizAttempt, related_name='responses', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(QuestionOption, null=True, blank=True, on_delete=models.CASCADE)
    short_answer_text = models.TextField(blank=True, null=True)
    is_correct = models.BooleanField()

    def __str__(self):
        return f"{self.attempt.user.username} - {self.question.text[:50]}"

