from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet

from .models import Hunt, Question, QuestionChoice, HuntSession, Player, Answer

#################### image related ##############

# from PIL import Image
# from django.core.files.uploadedfile import SimpleUploadedFile

from django.utils.translation import gettext as _


# The model forms for the huntSessions app

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["description", "question_type", "model_answer"]


class QuestionChoiceForm(forms.ModelForm):
    class Meta:
        model = QuestionChoice
        fields = ["option", "is_correct"]
        labels = {
            "option": "Answer option",
            "is_correct": "Correct answer"
        }


QuestionFormSet = inlineformset_factory(
    Question,
    QuestionChoice,
    form=QuestionChoiceForm,
    extra=4,
    can_delete=True
)

EditQuestionFormSet = inlineformset_factory(
    Question,
    QuestionChoice,
    form=QuestionChoiceForm,
    extra=0,
    can_delete=True
)


class HuntForm(forms.ModelForm):
    questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Hunt
        fields = ["hunt_name", "location", "questions"]


class HuntSessionForm(forms.ModelForm):
    class Meta:
        model = HuntSession
        fields = ["hunt", "status", "join_code"]

class JoinCodeForm(forms.Form):
    join_code = forms.CharField(max_length=6, min_length=6, label= "Join Code",
        widget=forms.TextInput(attrs={"placeholder": "Enter the join code"}))

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ["name"]
        labels = {"name": "Team Name"}
        widgets = {"name": forms.TextInput(attrs={
            "placeholder": "Enter your team name",
            "minlength": 2,
            "maxlength": 30
        })}

class ShortAnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["answer"]
        labels = {"answer": "Your Answer"}
        widgets = {"answer": forms.TextInput(attrs={"placeholder": "Type your answer here..."})}

class MultipleChoiceForm(forms.ModelForm):
    # Display multiple-choice answers as radio buttons,
    # allowing the student to select one option

    class Meta:
        model = Answer
        fields = ["choice"]
        widgets = {"choice": forms.RadioSelect}
        labels = {"choice": "Select an Option:"}

    def __init__(self, *args, question=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["choice"].empty_label = None

        if question is not None:
            self.fields["choice"].queryset = question.choices.all()


class PictureForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["picture"]
        widgets = {
            "picture": forms.ClearableFileInput(
                attrs={"accept": "image/*"}
            )
        }
        labels = {"picture": "Upload a Photo"}

class MarkAnswersForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["is_correct"]


MarkAnswersFormSet = inlineformset_factory(
    Player,
    Answer,
    fields=["is_correct"],
    extra=0,
    can_delete=False
)


# A function for cleaning up picture submissions and restricting uploads

'''
def CleanPicture():
        picture = self.cleaned_data.get('picture',False)
        #check the photo's parameters and only accpet what fits crieteria

        if piacture:
            #get parameters for diemensions
            img = Image.open(picture)
            width, height = img.size

            #if required any dimension restrictions can be checked with the above parameter values

            #validate content types or extensions of image files
            #if theres any other accepted image types add to the list in if statement
            main, sub = picture.content_type.split('/')
            if not (main=='picture' and sub.lower() in ['jpeg', 'pjpeg', 'png', 'jpg']):
                raise forms.ValidationError(_('Please use a JPEG or PNG image.'))
            #check an rgb picture at these resolution for a size check
            if len(picture) >(3*1024*1024*1.6):
                raise forms.ValidationError(_('Image file too large ( maximum 5mb )'))

        else:
            raise forms.ValidationErrorraise(_("Couldn't read uploaded image"))
        return picture
'''
