from __future__ import unicode_literals

from django.db import models

class Events(models.Model):
    # By default, Django gives each model an ID
    event_name = models.CharField(max_length=100)
