
from django.contrib import admin
from .models import Trip, Step, Photo

class StepInline(admin.TabularInline):
	model = Step
	extra = 1

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'cover_photo')
	inlines = [StepInline]

@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'trip', 'cover_photo')

class PhotoInline(admin.TabularInline):
	model = Photo
	extra = 1

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'step', 'date')
