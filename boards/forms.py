from django import forms
from .models import Topic, Post


class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        label=u'内容',
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'What is on your mind?'}
        ),
        max_length=4000,
        help_text='最长4000字！'
    )

    class Meta:
        model = Topic
        fields = ('subject', 'message')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('message',)