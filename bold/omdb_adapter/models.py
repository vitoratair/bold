from __future__ import unicode_literals
from django.db import models

class Mapper(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    mapper = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name
