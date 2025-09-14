
from django.contrib import admin
from .models import Trip, Step, Photo
from django.utils.html import format_html


class StepInline(admin.TabularInline):
	model = Step
	extra = 1
	readonly_fields = ("order",)
	fields = ("name", "order", "description", "lat", "lng", "cover_photo")

class PhotoInline(admin.TabularInline):
	model = Photo
	extra = 1

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "cover_photo")
	inlines = [StepInline]

@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "trip", "order", "cover_photo", "photo_count")
	ordering = ("trip", "order")
	readonly_fields = ("order",)
	inlines = [PhotoInline]

	def photo_count(self, obj):
		return obj.photos.count()

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "step", "date", "thumbnail")

	def thumbnail(self, obj):
		if obj.url:
			return format_html('<img src="{}" style="height:40px;width:auto;object-fit:cover;" />', obj.url)
		return ""
