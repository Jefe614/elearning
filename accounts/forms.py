# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    grade_level = forms.IntegerField(min_value=1, max_value=12)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'grade_level']

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
