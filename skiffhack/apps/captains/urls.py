
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to
import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', views.Captaincies.as_view(), name="captain-list"),
    url(r'^[.](?P<format>json|html)$', views.Captaincies.as_view(), name="captain-list"),
)
