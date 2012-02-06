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

class JSONOrHTMLMixin(object):
    def dispatch(self, request, *args, **kwargs):
        format = kwargs.pop("format","html")
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        method = request.method.lower()
        if method in self.http_method_names:
            if format != "html":
                method += "_" + format
            handler = getattr(self, method, self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        self.request = request
        self.args = args
        self.kwargs = kwargs
        return handler(request, *args, **kwargs)
    
    def get_json(self, request, *args, **kwargs):
        json_data = json.dumps(self.get_json_data(), sort_keys=True, indent=4)
        if "callback" in self.request.GET:
            callback = request.GET["callback"]
            assert re.match("^[a-zA-Z0-9_]*$", callback)
            json_data = "%s(%s)" % (callback, json_data);
        return HttpResponse(json_data)

    def get_context_data(self, **kwargs):
        context = super(JSONOrHTMLMixin, self).get_context_data(**kwargs)
        context.update(self.get_json_data())
        return context

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

    def get_jpg(self):
        self.object = self.get_object()
        return HttpResponseRedirect(self.object.profile_image())
