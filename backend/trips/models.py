
from django.db import models

class Trip(models.Model):
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name

class Step(models.Model):
	trip = models.ForeignKey(Trip, related_name='steps', on_delete=models.CASCADE)
	name = models.CharField(max_length=255)

	def __str__(self):
		return f"{self.name} ({self.trip.name})"
