from django.shortcuts import render, get_object_or_404
from .models import Profile
from thoughts.models import Thought
from django import http
from django.core.urlresolvers import reverse, reverse_lazy
from .forms import ProfileForm
from django.db.models import Count
from datetime import date



#redirects to user's profile
def profile_proxy(request):
    return http.HttpResponseRedirect(request.user.profile.get_absolute_url())



def profile_detail(request, pk):
  if request.method == 'GET':
    try:
      profile = Profile.objects.get(user_id=pk)
      thoughts = Thought.objects.filter(user_id=pk).order_by('-date') #user's thoughts
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
        return http.HttpResponseRedirect(reverse('accounts:profile-detail', kwargs={'pk': request.user.pk}))
      else:
        return http.HttpResponseRedirect(reverse_lazy('thoughts:index'))
    return render(request, 'thoughts/profile.html', {"profile": profile, "thoughts": thoughts, "statuses_data": statuses_data})



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

      return http.HttpResponseRedirect(profile.get_absolute_url())

    return render(request, 'thoughts/profile.html', {'form': form, 'profileUpdate': profile})
  else:
    return http.HttpResponseRedirect(reverse_lazy('thoughts:index'))

