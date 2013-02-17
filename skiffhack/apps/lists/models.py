from django.db import models
from profiles.models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed
import requests
from django.conf import settings

class List(models.Model):
    address = models.EmailField()
    description = models.CharField()
    subscribers = models.ManyToManyField(User)
    
def subscribers_changed(sender, **kwargs):
    lst = kwargs["instance"]
    action = kwargs["action"]
    if action not in ["pre_add", "pre_remove"]:
        return
    users = [User.objects.get(id=x) for x in kwargs["pk_set"]]
    
    for user in users:
        if action == "pre_add":
            requests.post(
                "https://api.mailgun.net/v2/lists/%s/members" % (lst.address,),
                auth=('api', settings.MAILGUN_API_KEY),
                data={'subscribed': True,
                      'address': user.email,
                      'name': "%s %s" % (user.first_name, user.last_name),})
                      # 'description': 'Developer',
                      # 'vars': '{"age": 26}'})
        elif action == "pre_remove": 
            requests.delete(
                "https://api.mailgun.net/v2/lists/%s/members/%s" % (lst.address, email,),
                auth=('api', settings.MAILGUN_API_KEY))

    
m2m_changed.connect(subscribers_changed, sender=List.subscribers.through)
