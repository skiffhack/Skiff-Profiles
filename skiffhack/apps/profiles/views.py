from django.views.generic import UpdateView, View
from models import *
import forms
from django.utils import simplejson as json
from django.http import HttpResponse
import re

class EditProfile(UpdateView):
    model = Profile
    template_name = "edit_profile.html"
    form_class = forms.ProfileForm
    success_url = "/"

    def get_object(self):
        profile, _created = Profile.objects.get_or_create(user=self.request.user)
        return profile


class JSONView(View):
    def get(self, request, *args, **kwargs):
        json_data = json.dumps(self.get_data(request, *args, **kwargs))
        if "callback" in request.GET:
            callback = request.GET["callback"]
            assert re.match("^[a-zA-Z0-9_]*$", callback)
            json_data = "%s(%s)" % (callback, json_data);
        return HttpResponse(json_data)

class ProfileAPI(JSONView):
    def get_data(self, request, email):
        profile = Profile.objects.get(user__email=email)
        details = {}
        for field in ["real_name", "twitter", "what_do_you_do", "about_me"]:
            details[field] = getattr(profile, field)
        return details
