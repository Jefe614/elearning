# gamification/views.py
from django.shortcuts import render
from django.contrib.auth import get_user_model
from .models import Badge, UserBadge
from quizzes.models import QuizAttempt

def badge_list(request):
    badges = Badge.objects.all()
    user_badges = UserBadge.objects.filter(user=request.user)
    return render(request, 'badge_list.html', {
        'badges': badges,
        'user_badges': user_badges
    })

def leaderboard(request):
    User = get_user_model()
    top_users = User.objects.annotate(
        total_score=models.Sum('quizattempt__score')
    ).order_by('-total_score')[:10]
    return render(request, 'leaderboard.html', {
        'top_users': top_users
    })