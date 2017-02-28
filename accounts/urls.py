from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'accounts'



urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uid64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^profile/$', login_required(views.profile_proxy), name='profile-proxy'),
    url(r'^profile/(?P<pk>[0-9]+)/$', views.profile_detail, name='profile-detail'),
    url(r'^profile/update/(?P<pk>[0-9]+)/$', views.profile_update, name='profile-update'),
]