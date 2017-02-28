from django.db import models
from django.core.urlresolvers import reverse
from django_countries.fields import CountryField
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE,
        primary_key=True,
    )
    birthday = models.DateField(null = True)
    country = CountryField(blank_label='(select country)', null = True)
    gender = models.CharField(
        choices=(
            ('m', 'Male'),
            ('f', 'Female'),
        ),
        max_length=1,
        null = True
    )
    avatar = models.FileField(  #imagefield later https://github.com/matthewwithanm/django-imagekit
        upload_to='avatars',
        default='/avatars/default-avatar.png'
    )
    email_confirmed = models.BooleanField(default=False)


    def is_filled(self):
        if self.birthday and self.country and self.gender:
            return True
        else:
            return False


    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


    def get_absolute_url(self):
        return reverse('accounts:profile-detail', kwargs={'pk': self.user_id})