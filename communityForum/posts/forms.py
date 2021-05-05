from django import forms

from .models import Answer, Topic

class CreateTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = [
            'title', 'description'
        ]

class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = [
            'body', 'author', 'post', 'tags'
        ]