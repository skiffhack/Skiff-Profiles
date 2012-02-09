from django.views.generic import UpdateView, View, DetailView, ListView
from models import *
import forms
from django.utils import simplejson as json
from django.http import HttpResponse, HttpResponseRedirect
import re
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import urllib, hashlib
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404
from shared.views import JSONOrHTMLMixin

class EditProfile(UpdateView):
    model = Profile
    template_name = "skiffprofiles/edit_profile.html"
    form_class = forms.ProfileForm
    success_url = "/profile/me.html"

    def get_object(self):
        profile, _created = Profile.objects.get_or_create(user=self.request.user)
        return profile
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EditProfile, self).dispatch(*args, **kwargs)

class ProfileList(JSONOrHTMLMixin, ListView):
    template_name = "skiffprofiles/profile_list.html"
    model = Profile
    context_object_name = "profile_list"
    queryset = Profile.objects.exclude(real_name="").order_by("real_name")

    def get_json_data(self):
        return {"profiles": [profile.to_json() for profile in self.get_queryset().all()]}

def profile_by_email(request, profile, format):
    object = get_object_or_404(Profile,user__email=profile)
    return HttpResponseRedirect(reverse("profile", kwargs={"profile": object.hash, "format": format}))
                                
@login_required
def own_profile(request, format):
    object = get_object_or_404(Profile, user=request.user)
    return HttpResponseRedirect(reverse("profile", kwargs={"profile": object.hash, "format": format}))

class ViewProfile(JSONOrHTMLMixin, DetailView):
    context_object_name = "profile"
    template_name = "skiffprofiles/view_profile.html"
    
    def get_object(self):
        return get_object_or_404(Profile,hash=self.kwargs["profile"])
    
    def get_json_data(self):
        if not hasattr(self, "object"):
            self.object = self.get_object()
        return self.object.to_json()

    def get_jpg(self, request, *args, **kwargs):
        self.object = self.get_object()
        return HttpResponseRedirect(self.object.profile_image())
