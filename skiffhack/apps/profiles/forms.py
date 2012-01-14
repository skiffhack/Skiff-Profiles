from bootstrap.forms import BootstrapForm,BootstrapModelForm,Fieldset
from models import *

class ProfileForm(BootstrapModelForm):
    class Meta:
        model = Profile
        exclude = ("user","slug",)
