#local datetime

from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Thought(models.Model):
  text = models.TextField()
  date = models.DateTimeField(default=datetime.now)
  status = models.CharField(
      max_length=8,
      choices=(
        ('negative', 'Negative'),
        ('positive', 'Positive'),
        ('neutral', 'Neutral')
      ),
      default = 'neutral'
  )
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.text

  def get_absolute_url(self):
    return reverse('thoughts:detail', kwargs={'pk': self.pk})


class Comment(models.Model):
  text = models.TextField()
  date = models.DateTimeField(default=datetime.now)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  thought = models.ForeignKey(Thought, on_delete=models.CASCADE)

  def __str__(self):
    return self.text
