from django import forms
from .models import Hunt
from .models import Question
from .models import HuntSession
from .models import Player
####################imgae related##############



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

class JoinCodeForm(forms.Form):
        join_code = forms.CharField(max_length=6,min_length=6)

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ["name"]
'''
class SubmitPicture(forms.Form):
    file = FileField()

'''