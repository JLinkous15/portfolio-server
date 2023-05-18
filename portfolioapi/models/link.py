from django.db import models


class Link(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    external = models.BooleanField(default=False)
