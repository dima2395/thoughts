from django import forms
from .models import Profile
import datetime

class ProfileForm(forms.ModelForm):

  #birthday = forms.DateField(widget=forms.TextInput(attrs={'placeholder': 'format: 1995-01-30'}))
  year = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'example 1995'}))
  month = forms.ChoiceField(choices=[(i, datetime.date(2017, i, 1).strftime('%B')) for i in range(1, 13)]) #generates months
  day = forms.ChoiceField(choices=[(x,x)for x in range(1,32)]) #generates days 1-31
  
  class Meta:
    model = Profile
    fields=['year', 'month', 'day', 'country', 'gender', 'avatar']


  def clean_year(self):
    year = int(self.cleaned_data['year'])
    current_year = datetime.date.today().year
    if year <= 0:
      raise forms.ValidationError('Year must be greater than or equal 0')
    if year > current_year:
      raise forms.ValidationError('Year must be less than or equal to {}'.format(current_year))
    return year

  def clean(self):
    cleaned_data = super(ProfileForm, self).clean()
    year = cleaned_data.get('year')
    month = int(cleaned_data.get('month'))
    day = int(cleaned_data.get('day'))

    if year:
      current_date  = datetime.date.today()
      bday = datetime.date(year, month, day)

      if bday > current_date:
        raise forms.ValidationError('Are you from future? :)')