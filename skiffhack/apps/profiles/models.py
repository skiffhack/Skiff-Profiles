from django.db import models
from django.contrib.auth.models import *
from django.template import defaultfilters
import hashlib, urllib
from django.core.urlresolvers import reverse
from django.conf import settings
import requests

class Profile(models.Model):
    """
    A user profile for someone at The Skiff. What should we include here?
    """
    hash = models.CharField(editable=False, max_length=64)
    user = models.OneToOneField(User)
    real_name = models.CharField(max_length=255, blank=True)
    twitter = models.CharField(max_length=255, blank=True)
    linkedin_url = models.CharField('LinkedIn URL', max_length=255, blank=True, help_text="The URL of your LinkedIn profile")
    github_url = models.CharField('GitHub URL', max_length=255, blank=True, help_text="The URL of your GitHub profile")
    url = models.CharField('URL', max_length=255, blank=True)
    about = models.TextField('Tell us about yourself', blank=True, help_text="Links are made clickable")
    what_do_you_do = models.TextField('What do you do?', blank=True, help_text="Links are made clickable")
    stuff_done = models.TextField("Show us some stuff you've made", blank=True, help_text="Links are made clickable")
    use = models.TextField("How do you use The Skiff?", blank=True, help_text="Links are made clickable")

    track_presence = models.BooleanField('Enable Skiff Presence', default=False, help_text="Remember my computer and use it to show when I'm online at The Skiff. Please do say yes to this, it's going to enable some cool stuff!")

    twitter_img_url = models.CharField(max_length=255, blank=True, null=True)

    def profile_image(self, size=80):
        """
        Return a profile image URL. It uses the gravatar image
        (indexed by email) with the default set to the user's Twitter
        profile image.
        """
        
        gravatar_url = "http://www.gravatar.com/avatar/" + self.hash + "?"
        options = {'s':str(size)}
        # Twitter have changed their API so this doesn't work anymore
        if self.twitter_img_url:
            options["d"] = self.twitter_img_url
        gravatar_url += urllib.urlencode(options)

        return gravatar_url


    def save(self, *args, **kwargs):
        self.hash = hashlib.md5(self.user.email.lower()).hexdigest()
        if self.twitter:
            if not self.twitter_img_url:
                twitter_url = "http://twitter.com/api/users/profile_image/?"
                twitter_url += urllib.urlencode({"screen_name": self.twitter, "size": "bigger"})
                try:
                    self.twitter_img_url = requests.get(twitter_url).headers["Location"]
                except Exception, e:
                    print "Failure to get twitter profile image :("
                    print e
            else:
               self.twitter_img_url = None
        return super(Profile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("profile", kwargs={"profile": self.hash, "format": "html"})


    def to_json(self):
        """
        Convert to JSON suitable for sending to the client
        """
        details = {}
        for field in ["real_name", "twitter", "what_do_you_do", "about", "url", "hash", "linkedin_url", "github_url", "track_presence", "stuff_done","use"]:
            details[field] = getattr(self, field)
        details["profile_image"] = self.profile_image()
        # Link to the json and html versions of this self
        for format in ["json","html"]:
            details[format] = settings.SITE_URL + reverse("profile", kwargs={"format": format, "profile": self.hash})
        details["href"] = details["json"]
        details["twitter_link"] = "http://twitter.com/#!/%s" % (self.twitter,) if self.twitter else None
        details["status_link"] = "http://crane.papercreatures.com/status/" + self.hash
        # if self.request.user.is_authenticated():
        #     details["email"] = object.user.email
        return details

    def __unicode__(self):
        return self.real_name
