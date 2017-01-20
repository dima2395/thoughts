from django import forms
from django.forms import extras
from .models import Profile

class ProfileForm(forms.ModelForm):
  birthday = forms.DateField(widget=extras.SelectDateWidget(year=[for x in range(1900, 2005)]))
  class Meta:
    model = Profile
    exclude = ['user']
