
from django.db import models

class Trip(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField(blank=True, null=True)
	started_at = models.DateTimeField(auto_now_add=True)
	ended_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

class Step(models.Model):
	trip = models.ForeignKey(Trip, related_name='steps', on_delete=models.CASCADE)
	description = models.TextField(blank=True, null=True)
	started_at = models.DateTimeField(auto_now_add=True)
	ended_at = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=255)
	latitude = models.FloatField(blank=True, null=True)
	longitude = models.FloatField(blank=True, null=True)

	def __str__(self):
		return f"{self.name} ({self.trip.name})"
