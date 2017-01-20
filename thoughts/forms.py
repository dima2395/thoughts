from django import forms
from .models import Comment, Thought

class CommentForm(forms.ModelForm):
  text = forms.CharField(widget=forms.Textarea(attrs={'rows': 6, 'cols': 40}), label='')
  class Meta:
    model = Comment
    fields = ['text']


class ThoughtForm(forms.ModelForm):
  text = forms.CharField(widget=forms.Textarea(attrs={'rows': 8, 'cols': 40}), label='')
  class Meta:
    model = Thought
    fields = ['text', 'status']