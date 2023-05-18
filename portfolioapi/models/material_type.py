from django.db import models


class MaterialType(models.Model):
    name = models.CharField(max_length=25)
