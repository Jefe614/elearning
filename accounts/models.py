# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Additional user fields specific to Quizzy
    grade_level = models.IntegerField(null=True, blank=True)
    total_points = models.IntegerField(default=0)