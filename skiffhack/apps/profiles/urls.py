from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to
import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    (r'^edit_profile/$', views.EditProfile.as_view()),
    url(r'^$', views.ProfileList.as_view(), name="profile-list"),
    url(r'^[.](?P<format>json|html)$', views.ProfileList.as_view(), name="profile-list"),
    url(r'^me[.](?P<format>html|json|jpg)$', views.own_profile),
    url(r'^(?P<profile>.*@.*)[[.](?P<format>html|json|jpg)$', views.profile_by_email),
    url(r'^(?P<profile>.*)[.](?P<format>html|json|jpg)$', views.ViewProfile.as_view(), name="profile"),
)
