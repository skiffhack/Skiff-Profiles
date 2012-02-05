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

class ProfileList(ListView):
    template_name = "skiffprofiles/profile_list.html"
    model = Profile
    context_object_name = "profile_list"
    queryset = Profile.objects.exclude(real_name="").order_by("real_name")
    

class JSONOrHTMLView(DetailView):
    def get(self, request, *args, **kwargs):
        format = kwargs.pop("format","html")
        self.object = self.get_object()
        return getattr(self, "render_%s" % (format,), self.render_html)()

    def render_html(self):
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def render_json(self):
        json_data = json.dumps(self.get_json_data(object=self.object))
        if "callback" in self.request.GET:
            callback = request.GET["callback"]
            assert re.match("^[a-zA-Z0-9_]*$", callback)
            json_data = "%s(%s)" % (callback, json_data);
        return HttpResponse(json_data)

    def get_context_data(self, object):
        context = super(JSONOrHTMLView, self).get_context_data(object=object)
        context.update(self.get_json_data(object=object))
        return context

def profile_by_email(request, profile, format):
    object = get_object_or_404(Profile,user__email=profile)
    return HttpResponseRedirect(reverse("profile", kwargs={"profile": object.hash, "format": format}))
                                
@login_required
def own_profile(request, format):
    object = get_object_or_404(Profile, user=request.user)
    return HttpResponseRedirect(reverse("profile", kwargs={"profile": object.hash, "format": format}))

class ViewProfile(JSONOrHTMLView):
    context_object_name = "profile"
    template_name = "skiffprofiles/view_profile.html"
    
    def get_object(self):
        return get_object_or_404(Profile,hash=self.kwargs["profile"])
    
    def get_json_data(self, object):
        profile = object
        details = {}
        for field in ["real_name", "twitter", "what_do_you_do", "about", "url", "hash"]:
            details[field] = getattr(profile, field)
        details["profile_image"] = profile.profile_image()
        # Link to the json and html versions of this profile
        for format in ["json","html"]:
            details[format] = settings.SITE_URL + reverse("profile", kwargs={"format": format, "profile": profile.hash})
        details["twitter_link"] = "http://twitter.com/#!/%s" % (profile.twitter,) if profile.twitter else None
        if self.request.user.is_authenticated():
            details["email"] = object.user.email
        return details

    def render_jpg(self):
        return HttpResponseRedirect(self.object.profile_image())
