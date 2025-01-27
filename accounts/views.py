# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model
from quizzes.models import Quiz
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm

User = get_user_model()

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        grade_level = request.POST['grade_level']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        # Check if username is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register')

        # Check if email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('register')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Registration successful! You can now log in.")
        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'], 
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('subject_selection')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def profile(request):
    attempts = request.user.quizattempt_set.all()
    badges = request.user.userbadge_set.all()
    return render(request, 'profile.html', {
        'attempts': attempts,
        'badges': badges
    })


def select_occupation(request):
    if request.method == 'POST':
        occupation = request.POST.get('occupation')
        request.user.occupation = occupation
        request.user.save()
        if occupation == 'school':
            return redirect('select_role')
    return render(request, 'select_occupation.html')


# @login_required
def select_role(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        request.user.role = role
        request.user.save()
        if role == 'student':
            return redirect('student_details')
    return render(request, 'select_role.html')

# @login_required
def student_details(request):
    if request.method == 'POST':
        age = request.POST.get('age')
        request.user.age = age
        request.user.save()
        return redirect('login')  # Redirect to login after saving details
    return render(request, 'student_details.html')


