from django.db import models


class Trip(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=False, null=False)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(auto_now_add=True)
    # cover_photo added later to avoid circular import; defined after Photo class is declared via string reference
    cover_photo = models.ForeignKey('trips.Photo', related_name='cover_for_trips', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
