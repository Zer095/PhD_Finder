from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
import datetime

# Create your models here.

# Class that stores all the info about a PhD position
class Position(models.Model):
    # Title of the PhD position
    pos_title = models.CharField(max_length=200)
    # Academic field of the position
    pos_field = ArrayField(models.CharField(max_length=200), null=True, default=list)
    # Description of the PhD position, visible when you inspect
    # the specific position
    pos_desc = models.CharField(max_length=5000)
    # Institution/University that host the position
    pos_host = models.CharField(max_length=200)
    # Country where the position is available
    pos_country = ArrayField(models.CharField(max_length=200), null=True, default=list)
    # Date when the position has been published
    pos_pub_date = models.DateTimeField('date published')
    # Date whe the position will expire
    pos_exp_date = models.DateTimeField('date expiring')
    # Link of the PhD application
    pos_link = models.URLField(max_length=200, default="https://www.ice.csic.es/")

    # --------Methods of the class Position--------------------
    # Position that return the position title when we look for it
    def __str__(self):
        return self.pos_title
    
    # method that check if the position is still available
    def is_expired(self):
        now = timezone.now()
        return now >= self.pos_exp_date
    
    # method that check if the position is recent
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=5) <= self.pos_pub_date <= now