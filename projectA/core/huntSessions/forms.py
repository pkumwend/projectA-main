from django import forms
from .models import Hunt
from .models import Question
from .models import HuntSession

#the model fors for the huntSessions app

 

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["description","question_type"]


class HuntForm(forms.ModelForm):
    questions = forms.ModelMultipleChoiceField(queryset=Question.objects.all(),widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Hunt
        fields = ["hunt_name","location","questions"]
        
class HuntSessionForm(forms.ModelForm):
    class Meta:
        model = HuntSession
        fields = ["hunt","status","join_code"]