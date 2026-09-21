from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet

from .models import Hunt
from .models import Question, QuestionChoice
from .models import HuntSession
from .models import Player

from .models import QuestionChoice, Answer

####################imgae related##############

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


#the model fors for the huntSessions app



class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["description","question_type"]
class QuestionChoiceForm(forms.ModelForm):
    class Meta:
        model = QuestionChoice
        fields = ["option", "is_correct"]
        labels = {"option":"answer option",
                    "is_correct": "correct answer"}


QuestionFormSet = inlineformset_factory(
    Question,QuestionChoice,
        form = QuestionChoiceForm,
        extra=4,
        can_delete=True)
EditQuestionFormSet = inlineformset_factory(
    Question,QuestionChoice,
        form=QuestionChoiceForm,
        extra=0,
        can_delete=True)

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

##### answer forms #########
class ShortAnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["answer"]

class MultipleChoiceForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["choice"]


class PictureForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["picture"]
         
