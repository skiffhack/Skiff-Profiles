from bootstrap.forms import BootstrapForm,BootstrapModelForm,Fieldset
from models import *
from django import forms

class ProfileForm(BootstrapModelForm):
    class Meta:
        model = Profile
        exclude = ("user","hash",)
    url = forms.URLField()
    twitter = forms.RegexField(regex="^[a-zA-Z0-9_]+$", required=False, error_message="Please enter just your Twitter id, leave off the @")
