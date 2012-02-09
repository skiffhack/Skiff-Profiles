from django.views.generic import UpdateView, TemplateView, DetailView, ListView
from models import *
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
import models
import datetime


class Captaincies(JSONOrHTMLMixin, TemplateView):
    template_name = "captains/captaincies.html"
    def dispatch(self, request, *args, **kwargs):
        starts_on = datetime.date.today()-datetime.timedelta(7)
        ends_on = starts_on + datetime.timedelta(30*6)
        self.captaincies = list(models.Captaincy.objects.all_in_date_range(starts_on,ends_on))
        return super(Captaincies, self).dispatch(request, *args, **kwargs)

    def get_json_data(self):
        lst = [captaincy.to_json()
                  for captaincy in
                   self.captaincies]
        return {"captaincies": lst}
        
    def get_context_data(self):
        context = super(Captaincies, self).get_context_data()
        context["captaincies"] = self.captaincies
        return context
