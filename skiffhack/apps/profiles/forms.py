from bootstrap.forms import BootstrapForm,BootstrapModelForm,Fieldset
from models import *
from django import forms

class ProfileForm(BootstrapModelForm):
    class Meta:
        model = Profile
        exclude = ("user","hash",)
    url = forms.URLField(required=False)
    github_url = forms.URLField(required=False)
    linkedin_url = forms.URLField(required=False)
    twitter = forms.RegexField(regex="^[a-zA-Z0-9_]+$", required=False, error_message="Please enter just your Twitter id, leave off the @")
