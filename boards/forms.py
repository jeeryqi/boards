from django import forms
from .models import Topic

class NewTopicForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(), max_length=4000)

    class Meata:
        model = Topic
        fields = ('subject', 'message')