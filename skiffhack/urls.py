from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from profiles import views
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', direct_to_template, {'template': 'demo.html'}),
    (r'^edit_profile/', views.EditProfile.as_view()),
    (r'^api/profile/(.*)', views.ProfileAPI.as_view()),
    (r'^browserid/', include('django_browserid.urls')),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {"next_page": "/"}, name="logout"),
    url(r'^admin/', include(admin.site.urls)),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
