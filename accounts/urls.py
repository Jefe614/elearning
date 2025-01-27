from . import views
from django.urls import path

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('register/occupation/', views.select_occupation, name='select_occupation'),
    path('register/role/', views.select_role, name='select_role'),
    path('register/student/', views.student_details, name='student_details'),
]