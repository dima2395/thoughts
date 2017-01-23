from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views import generic
from django import http
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Thought
from .forms import CommentForm, ThoughtForm
from django.contrib import messages


def index(request):
  step = 5

  if request.is_ajax(): # ajax call
    start = int(request.GET.get('start', None))
    end = start + step
    thoughts = get_list_or_404(Thought.objects.all().order_by('-date')[start:end])
    return render(request, 'thoughts/thought.html', {'thoughts': thoughts})

  else:  # index page 
    start = 0
    end = 3
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



