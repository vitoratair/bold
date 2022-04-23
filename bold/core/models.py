
from django.db import models


class Subscriber(models.Model):
    client = models.CharField(max_length=50)
    name = models.CharField(max_length=50, null=False, blank=False)
    resource = models.CharField(max_length=50, null=False, blank=False)


    class Meta:
        ordering  = ('name',)

    def __str__(self):
        return "%s - %s" % (self.name, self.resource)
