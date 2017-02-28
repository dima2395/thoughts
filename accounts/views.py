from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile
from thoughts.models import Thought
from django import http
from django.core.urlresolvers import reverse, reverse_lazy
from .forms import ProfileForm, SignUpForm
from django.db.models import Count
from datetime import date
from django.contrib.auth import login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


#redirects to user's profile
def profile_proxy(request):
    return http.HttpResponseRedirect(request.user.profile.get_absolute_url())



def profile_detail(request, pk):
    if request.method == 'GET':
        try:
            profile = Profile.objects.get(user_id=pk)
            thoughts = Thought.objects.filter(user_id=pk).order_by('-date')  # user's thoughts
            statuses = Thought.objects.filter(user_id=pk).values('status').annotate(count=Count('id'))
            statuses_data = {}
            statuses_data['labels'] = []
            statuses_data['values'] = []
            statuses_data['bgcolors'] = []

            for status in statuses:
                statuses_data['labels'].append(status['status'].capitalize())
                statuses_data['values'].append(status['count'])
                if status['status'] == 'neutral':
                    statuses_data['bgcolors'].append('rgba(230, 230, 230, 0.76)')
                elif status['status'] == 'positive':
                    statuses_data['bgcolors'].append('rgba(185, 255, 171, 0.76)')
                elif status['status'] == 'negative':
                    statuses_data['bgcolors'].append('rgba(255, 187, 198, 0.76)')

        except Profile.DoesNotExist:
            if request.user.is_authenticated():
                return redirect(reverse('accounts:profile-detail', kwargs={'pk': request.user.pk}))
            else:
                return redirect(reverse_lazy('thoughts:index'))
        return render(request, 'thoughts/profile.html',
                          {"profile": profile, "thoughts": thoughts, "statuses_data": statuses_data})



def profile_update(request, pk):
  profile = get_object_or_404(Profile, pk=pk)

  try:
    u_year = profile.birthday.year #check if date exist
    u_month = profile.birthday.month
    u_day = profile.birthday.day
  except:
    u_year = None # u - user
    u_month = None
    u_day = None

  form = ProfileForm(request.POST or None, request.FILES or None, instance=profile, initial={
                      'year':u_year,
                      'month': u_month,
                      'day': u_day
                    })

  if profile.user == request.user:

    if form.is_valid():
      year = int(form.cleaned_data['year'])
      month = int(form.cleaned_data['month'])
      day = int(form.cleaned_data['day'])

      profile = form.save(commit=False)
      profile.birthday = date(year, month, day)
      profile.save()

      return redirect(profile.get_absolute_url())

    return render(request, 'thoughts/profile.html', {'form': form, 'profileUpdate': profile})
  else:
    return redirect(reverse_lazy('thoughts:index'))


def signup(request):
    if request.user.is_authenticated():
        logout(request)
        return http.HttpResponseRedirect(reverse('accounts:signup'))

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('registration/activation_email.txt', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            try:
                user.email_user(subject, message)
                messages.success(request, 'Email was sent successful')
            except:
                messages.error(request, 'Error, email was not sent, try again')
                return render(request, 'registration/registration_form.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'registration/registration_form.html', {'form': form})



def activate(request, uid64, token):
    logout(request)

    if uid64 and token:
        uid = urlsafe_base64_decode(uid64)
        try:
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.info(request, 'Welcome {}, please fill your profile'.format(user.username))
            return http.HttpResponseRedirect(reverse('accounts:profile-update', kwargs={'pk': user.pk}))
        else:
            return http.HttpResponseRedirect(reverse_lazy('thoughts:index'))















