from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'thoughts'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^add/$', login_required(views.create), name='thought-add'),
    url(r'^edit/(?P<pk>[0-9]+)/$', login_required(views.update), name='thought-update'),
    url(r'^delete/(?P<pk>[0-9]+)/$', login_required(views.delete), name='thought-delete'),
]