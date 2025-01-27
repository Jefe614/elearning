from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('subject_selection', views.subject_selection, name='subject_selection'),
    path('quiz_list', views.quiz_list, name='quiz_list'),
    path('quiz/create/', views.quiz_create, name='quiz_create'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:quiz_id>/attempt/', views.quiz_attempt, name='quiz_attempt'),
    path('quiz/<int:quiz_id>/results/', views.quiz_results, name='quiz_results'),
    path('subject/<str:subject>/', views.subject_quizzes, name='subject_quizzes'),
    path('mathematics/', views.mathematics_quiz, name='mathematics_quiz'),
    path('science/', views.science_quiz, name='science_quiz'),
    path('english/', views.english_quiz, name='english_quiz'),    
    # path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),

]