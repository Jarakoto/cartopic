from django.db import models
from .trip import Trip

class Step(models.Model):
    trip = models.ForeignKey(Trip, related_name='steps', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(editable=False, default=0, help_text="Sequence index within a trip starting at 0")
    description = models.TextField(blank=False, null=False)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    lat = models.FloatField(blank=False, null=False)
    lng = models.FloatField(blank=False, null=False)
    cover_photo = models.ForeignKey('trips.Photo', related_name='cover_for_steps', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.trip.name})"

    def save(self, *args, **kwargs):
        if self._state.adding and self.trip_id is not None:  # type: ignore[attr-defined]
            # Determine next order value for this trip
            last = Step.objects.filter(trip_id=self.trip_id).order_by('-order').first()  # type: ignore[attr-defined]
            self.order = 0 if not last else last.order + 1  # type: ignore[attr-defined]
        super().save(*args, **kwargs)
