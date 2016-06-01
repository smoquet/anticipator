from __future__ import unicode_literals

from django.db import models

class Events(models.Model):
    # By default, Django gives each model an ID
    event-name = models.Charfield(max_length=100)
