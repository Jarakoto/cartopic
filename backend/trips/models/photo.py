from django.db import models
from .step import Step

class Photo(models.Model):
    step = models.ForeignKey(Step, related_name='photos', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    url = models.URLField(max_length=500)

    def __str__(self):
        return self.name
