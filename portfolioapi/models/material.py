from django.db import models


class Material(models.Model):
    name = models.CharField(max_length=100)
    material_type = models.ForeignKey(
        to='MaterialType', on_delete=models.CASCADE, related_name='materials')
