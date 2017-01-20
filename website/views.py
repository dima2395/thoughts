from django import http
from django.urls import reverse_lazy


def index(request):
  return http.HttpResponseRedirect(reverse_lazy('thoughts:index'))