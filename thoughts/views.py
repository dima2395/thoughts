from django.shortcuts import render, get_object_or_404, get_list_or_404
from django import http
from django.urls import reverse_lazy, reverse
from .models import Thought
from .forms import CommentForm, ThoughtForm
from django.contrib import messages
from django.db.models import Count
from datetime import datetime, timedelta


def index(request):
    step = 5

    if request.is_ajax():  # ajax call
        start = int(request.GET.get('start', None))
        end = start + step
        thoughts = get_list_or_404(Thought.objects.all().order_by('-date')[start:end])
        return render(request, 'thoughts/thought.html', {'thoughts': thoughts})

    else:  # index page
        start = 0
        end = 5
        thoughts = Thought.objects.all().order_by('-date')[start:end]
        return render(request, 'thoughts/index.html', {'thoughts': thoughts, 'start_from': end, 'step': step})


def detail(request, pk):
    thought = get_object_or_404(Thought, pk=pk)

    if request.user.is_authenticated():

        if request.method == 'POST':
            commentForm = CommentForm(request.POST)

            if commentForm.is_valid():
                comment = commentForm.save(commit=False)
                comment.user = request.user
                comment.thought = Thought.objects.get(pk=pk)
                comment.save()
                return http.HttpResponseRedirect(reverse('thoughts:detail', kwargs={'pk': pk}))

        else:
            commentForm = CommentForm()

        return render(request, 'thoughts/detail.html', {
            'thought': thought,
            'commentForm': commentForm,
        })

    else:
        return render(request, 'thoughts/detail.html', {
            'thought': thought,
        })


def create(request):
    user = request.user
    if user.profile.is_filled():

        if request.method == 'POST':
            form = ThoughtForm(request.POST)

            if form.is_valid():
                thought = form.save(commit=False)
                thought.user = user
                thought.save()
                return http.HttpResponseRedirect(thought.get_absolute_url())
        else:
            form = ThoughtForm()

        return render(request, 'thoughts/thought_form.html', {'form': form})

    else:
        messages.error(request, 'Fill your profile')
        return http.HttpResponseRedirect(reverse('accounts:profile-update', kwargs={'pk': user.pk}))


def update(request, pk):
    thought = get_object_or_404(Thought, pk=pk)
    form = ThoughtForm(request.POST or None, instance=thought)

    if thought.user == request.user:

        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect(thought.get_absolute_url())

        return render(request, 'thoughts/thought_form.html', {'form': form, 'object': thought})

    else:
        return http.HttpResponseRedirect(reverse_lazy('thoughts:index'))


def delete(request, pk):
    thought = get_object_or_404(Thought, pk=pk)

    if request.method == 'POST':
        thought.delete()
        return http.HttpResponseRedirect(reverse_lazy('thoughts:index'))
    else:
        return http.HttpResponseRedirect(reverse_lazy('thoughts:index'))


def statistics(request):
    # statusChart
    statuses = Thought.objects.values('status').annotate(count=Count('id'))
    statuses_data = {
        'labels': [],
        'values': [],
        'bgcolors': []
    }

    for status in statuses:
        statuses_data['labels'].append(status['status'].capitalize())
        statuses_data['values'].append(status['count'])
        if status['status'] == 'neutral':
            statuses_data['bgcolors'].append('rgba(230, 230, 230, 0.76)')
        elif status['status'] == 'positive':
            statuses_data['bgcolors'].append('rgba(185, 255, 171, 0.76)')
        elif status['status'] == 'negative':
            statuses_data['bgcolors'].append('rgba(255, 187, 198, 0.76)')

    # genderChart
    genders = Thought.objects.values('user__profile__gender').annotate(count=Count('id'))
    genders_data = {
        'labels': [],
        'values': [],
        'bgcolors': []
    }

    for gender in genders:
        if gender['user__profile__gender'] == 'm':
            genders_data['labels'].append('Male')
            genders_data['bgcolors'].append('rgba(40, 126, 255, 0.65)')
        elif gender['user__profile__gender'] == 'f':
            genders_data['labels'].append('Female')
            genders_data['bgcolors'].append('rgba(249, 17, 220, 0.65)')
        genders_data['values'].append(gender['count'])

    # activityChart
    today = datetime.now().date()
    week_ago = today - timedelta(days=6)
    week_activity = Thought.objects.filter(date__gte=week_ago).extra({'published': 'date(date)'}).values('published').annotate(count=Count('id'))
    activity_data = {
        'labels': [],
        'values': []
    }

    dates = [today - timedelta(days=x) for x in range(0, 7)]  # list of dates (today - 7 days)
    published = {day['published']: day['count'] for day in week_activity}  # dict key=date value=count of thoughts per date

    for date in reversed(dates):
        if date in published:
            activity_data['labels'].append(date.strftime('%b %d'))
            activity_data['values'].append(published[date])
        else:
            activity_data['labels'].append(date.strftime('%b %d'))
            activity_data['values'].append(0)

    return render(request, 'thoughts/statistics.html',
                  {'statuses_data': statuses_data, 'genders_data': genders_data, 'activity_data': activity_data})
