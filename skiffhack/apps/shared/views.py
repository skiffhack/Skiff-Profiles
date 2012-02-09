import re

from django.http import HttpResponse
from django.utils import simplejson as json


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

