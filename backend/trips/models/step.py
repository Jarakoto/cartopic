from django.db import models
from .trip import Trip

class Step(models.Model):
    trip = models.ForeignKey(Trip, related_name='steps', on_delete=models.CASCADE)
    description = models.TextField(blank=False, null=False)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    lat = models.FloatField(blank=False, null=False)
    lng = models.FloatField(blank=False, null=False)
    cover_photo = models.ForeignKey('trips.Photo', related_name='cover_for_steps', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.trip.name})"
