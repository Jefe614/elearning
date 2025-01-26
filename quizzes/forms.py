# quizzes/forms.py
from django import forms
from .models import Quiz, Question, QuestionOption

class QuizCreationForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'subject', 'grade_level']

class QuizAttemptForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.quiz = kwargs.pop('quiz')
        super().__init__(*args, **kwargs)
        
        for question in self.quiz.questions.all():
            if question.question_type == 'MC':
                choices = [(opt.id, opt.text) for opt in question.options.all()]
                self.fields[f'question_{question.id}'] = forms.ChoiceField(
                    choices=choices, 
                    widget=forms.RadioSelect,
                    label=question.text
                )
            elif question.question_type == 'TF':
                self.fields[f'question_{question.id}'] = forms.ChoiceField(
                    choices=[(True, 'True'), (False, 'False')],
                    widget=forms.RadioSelect,
                    label=question.text
                )
            else:  # Short Answer
                self.fields[f'question_{question.id}'] = forms.CharField(
                    widget=forms.Textarea(attrs={'rows': 3}),
                    label=question.text
                )

    def calculate_score(self):
        total_questions = self.quiz.questions.count()
        correct_answers = 0

        for question in self.quiz.questions.all():
            user_answer = self.cleaned_data.get(f'question_{question.id}')
            
            if question.question_type == 'MC':
                correct_option = question.options.get(is_correct=True)
                if int(user_answer) == correct_option.id:
                    correct_answers += 1
            
            elif question.question_type == 'TF':
                correct_option = question.options.get(is_correct=True)
                if str(user_answer) == str(correct_option.text):
                    correct_answers += 1
        
        return (correct_answers / total_questions) * 100
