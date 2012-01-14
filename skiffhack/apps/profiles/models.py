from django.db import models
from django.contrib.auth.models import *
from django.template import defaultfilters

class Profile(models.Model):
    """
    A user profile for someone at The Skiff. What should we include here?
    """
    user = models.OneToOneField(User)
    real_name = models.CharField(max_length=255, blank=True)
    twitter = models.CharField(max_length=255, blank=True)
    what_do_you_do = models.TextField(blank=True)
    about_me = models.TextField(blank=True)

   
