from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'accounts'

urlpatterns = [
    url(r'^profile/$', login_required(views.profile_proxy), name='profile-proxy'),
    url(r'^profile/(?P<pk>[0-9]+)/$', views.profile_detail, name='profile-detail'),
    url(r'^profile/update/(?P<pk>[0-9]+)/$', views.profile_update, name='profile-update'),
]