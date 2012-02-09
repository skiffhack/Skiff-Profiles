from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to
from profiles import views
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', redirect_to, {'url': '/profiles/'}),
    (r'^profile/', redirect_to, {'url': '/profiles/'}),
    url(r'^profiles/', include('profiles.urls')),
    url(r'^captains/', include('captains.urls')),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {"next_page": "/"}, name="logout"),
    url(r'^admin/', include(admin.site.urls)),
    (r'^browserid/', include('django_browserid.urls')),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
