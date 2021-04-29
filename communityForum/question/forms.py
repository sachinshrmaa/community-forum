from django import forms
from .models import Answer, Question


class QuestionForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    content = forms.Textarea()

    class Meta:
        model = Question
        fields = ["title", "content", "tags", "status"]