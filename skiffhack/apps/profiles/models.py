from django.db import models
from django.contrib.auth.models import *
from django.template import defaultfilters
import hashlib, urllib
from django.core.urlresolvers import reverse

class Profile(models.Model):
    """
    A user profile for someone at The Skiff. What should we include here?
    """
    hash = models.CharField(editable=False, max_length=64)
    user = models.OneToOneField(User)
    real_name = models.CharField(max_length=255, blank=True)
    twitter = models.CharField(max_length=255, blank=True)
    linkedin_url = models.CharField('LinkedIn URL', max_length=255, blank=True, help_text="The URL of your LinkedIn profile")
    url = models.CharField('URL', max_length=255, blank=True)
    about = models.TextField('Tell us about yourself', blank=True)
    what_do_you_do = models.TextField('What do you do?', blank=True)

    def profile_image(self, size=80):
        """
        Return a profile image URL. It uses the gravatar image
        (indexed by email) with the default set to the user's Twitter
        profile image.
        """
        twitter_url = "https://api.twitter.com/1/users/profile_image?"
        twitter_url += urllib.urlencode({"screen_name": self.twitter, "size": "bigger"})
        
        gravatar_url = "http://www.gravatar.com/avatar/" + self.hash + "?"
        gravatar_url += urllib.urlencode({'d':twitter_url, 's':str(size)})

        return gravatar_url


    def save(self, *args, **kwargs):
        self.hash = hashlib.md5(self.user.email.lower()).hexdigest()
        return super(Profile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("profile", kwargs={"profile": self.hash, "format": "html"})
