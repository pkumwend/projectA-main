from django import forms
from .models import Hunt
from .models import Question

#the model fors for the huntSessions app

class HuntForm(forms.ModelForm):
    class Meta:
        model = Hunt
        fields = ["hunt_name","location"]

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["description","question_type"]