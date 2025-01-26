from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('quiz_list', views.quiz_list, name='quiz_list'),
    path('quiz/create/', views.quiz_create, name='quiz_create'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:quiz_id>/attempt/', views.quiz_attempt, name='quiz_attempt'),
    path('quiz/<int:quiz_id>/results/', views.quiz_results, name='quiz_results'),
]