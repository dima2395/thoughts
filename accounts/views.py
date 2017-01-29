from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views import generic
from .models import Profile
from thoughts.models import Thought
from django import http
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from .forms import ProfileForm
from django.db.models import Count



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



def profile_proxy(request):
  if request.method == 'GET':
    user = request.user
    try:
      getattr(user, 'profile')
    except Profile.DoesNotExist:
      user.profile = Profile(user=user)
      user.profile.save()
    return http.HttpResponseRedirect(user.profile.get_absolute_url())




def profile_update(request, pk):
  profile = get_object_or_404(Profile, pk=pk)
  form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)

  if profile.user == request.user:

    if form.is_valid():
      form.save()
      return http.HttpResponseRedirect(profile.get_absolute_url())

    return render(request, 'thoughts/profile.html', {'form': form, 'profileUpdate': profile})
  else:
    return http.HttpResponseRedirect(reverse_lazy('thoughts:index'))

