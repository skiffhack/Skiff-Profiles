from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to
from profiles import views
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', redirect_to, {'url': '/profile/'}),
    (r'^edit_profile/$', views.EditProfile.as_view()),
    url(r'^profile/$', views.ProfileList.as_view(), name="profile-list"),
    url(r'^profile/me[.](?P<format>html|json|jpg)$', views.own_profile),
    url(r'^profile/(?P<profile>.*@.*)[[.](?P<format>html|json|jpg)$', views.profile_by_email),
    url(r'^profile/(?P<profile>.*)[.](?P<format>html|json|jpg)$', views.ViewProfile.as_view(), name="profile"),
    (r'^browserid/', include('django_browserid.urls')),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {"next_page": "/"}, name="logout"),
    url(r'^admin/', include(admin.site.urls)),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
