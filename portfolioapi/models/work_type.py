from django.db import models


class WorkType(models.Model):
    name = models.CharField(max_length=100)
