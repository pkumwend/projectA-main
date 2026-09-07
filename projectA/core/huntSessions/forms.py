from django import forms
from .models import Hunt

#the model fors for the huntSessions app

class HuntForm(forms.ModelForm):
    class Meta:
        model = Hunt
        fields = ['hunt_name','location']