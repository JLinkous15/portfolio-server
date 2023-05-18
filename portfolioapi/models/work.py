from django.db import models


class Work(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images')
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    work_type = models.ForeignKey(
        to='WorkType', on_delete=models.CASCADE, related_name='works')
    materials = models.ManyToManyField(to='Material', related_name='works')
    links = models.ManyToManyField(to='Link', related_name='works')
