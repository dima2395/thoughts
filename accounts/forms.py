from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
  birthday = forms.DateField(widget=extras.SelectDateWidget)
  class Meta:
    model = Profile
    exclude = ['user']
