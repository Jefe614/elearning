# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Additional user fields specific to Quizzy
    grade_level = models.IntegerField(null=True, blank=True)
    occupation = models.CharField(max_length=20, choices=[
        ('school', 'School'),
        ('corporate', 'Corporate'),
        ('personal', 'Personal'),
    ], null=True, blank=True)
    role = models.CharField(max_length=20, choices=[
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('administrator', 'Administrator'),
    ], null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    total_points = models.IntegerField(default=0)