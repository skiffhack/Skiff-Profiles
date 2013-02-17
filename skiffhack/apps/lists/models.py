from django.db import models
from profiles.models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed
import requests
from django.conf import settings

class List(models.Model):
    address = models.EmailField()
    description = models.CharField(max_length=255)
    subscribers = models.ManyToManyField(User, blank=True)

    def __unicode__(self):
        return self.address
    
def subscribers_changed(sender, **kwargs):
    print kwargs
    lst = kwargs["instance"]
    action = kwargs["action"]
    if action not in ["post_add", "post_remove", "post_clear"]:
        return
    users = lst.subscribers.all()
    users_by_email = dict((u.email, u) for u in users)
    emails = set(u.email for u in users)

    existing = requests.get(
        "https://api.mailgun.net/v2/lists/%s/members" % (lst.address,),
        auth=('api', settings.MAILGUN_API_KEY)).json()["items"]
    existing = set(x["address"] for x in existing)

    to_add = emails.difference(existing)
    to_remove = existing.difference(emails)

    for email in to_add:
        user = users_by_email[email]
        requests.post(
            "https://api.mailgun.net/v2/lists/%s/members" % (lst.address,),
            auth=('api', settings.MAILGUN_API_KEY),
            data={'subscribed': True,
                  'address': user.email,
                  'name': "%s %s" % (user.first_name, user.last_name),})

    for email in to_remove:
        requests.delete(
            "https://api.mailgun.net/v2/lists/%s/members/%s" % (lst.address, email,),
            auth=('api', settings.MAILGUN_API_KEY))

    
m2m_changed.connect(subscribers_changed, sender=List.subscribers.through)
