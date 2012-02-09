from django.db import models
import datetime

def monday(d):
    weekday = d.weekday()
    return d-datetime.timedelta(weekday)

class CaptaincyManager(models.Manager):
    def all_in_date_range(self, starts_on, ends_on):
        """
        Get captaincy objects for every week in the date range given.
        """
        starts_on = monday(starts_on)
        d = starts_on
        while d < ends_on:
            captaincy,_created = Captaincy.objects.get_or_create(starts_on=d)
            yield captaincy
            d = d + datetime.timedelta(7)


class Captaincy(models.Model):
    """
    Who is captain for a given week? Each captaincy starts on a Monday and ends on a Sunday.
    """
    starts_on = models.DateField()
    # hash of the user's email address used to identify users
    hash = models.CharField(editable=False, max_length=64)
    
    objects = CaptaincyManager()
    
    def ends_on(self):
        "The Sunday after the Monday indicated in the starts_on"
        return self.starts_on + datetime.timedelta(6)

    def filled(self):
        """
        Has the captaincy been filled?
        """
        return self.hash != ""

    def past(self):
        """
        Is this captaincy in the past?
        """
        self.ends_on() < datetime.date.today()

    def open(self):
        return not self.past() and not self.filled()
    
    def to_json(self):
        return {"hash": self.hash,
                "starts_on": self.starts_on.isoformat(),
                "ends_on": self.ends_on().isoformat(),
                "past": self.past(),
                "filled": self.filled()}
