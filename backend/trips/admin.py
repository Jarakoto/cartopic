
from django.contrib import admin
from .models import Trip, Step

class StepInline(admin.TabularInline):
	model = Step
	extra = 1

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
	list_display = ('id', 'name')
	inlines = [StepInline]

@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'trip')
