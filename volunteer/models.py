from django.db import models
from django.core.exceptions import ValidationError
import os


def validate_media_file(value):
	valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mov', '.avi', '.mkv']
	ext = os.path.splitext(value.name)[1]  # Get file extension

	if ext.lower() not in valid_extensions:
		raise ValidationError(f"Invalid file type: {ext}. Only images and videos are allowed.")


class News(models.Model):
	media_content = models.FileField(upload_to='news_content', blank=True, null=True, validators=[validate_media_file])
	title = models.CharField(max_length=255)
	description = models.TextField()
	address = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)


class Event(models.Model):
	media_content = models.FileField(upload_to='event_content', blank=True, null=True, validators=[validate_media_file])
	title = models.CharField(max_length=255)
	description = models.TextField()
	address = models.CharField(max_length=255)
	event_type = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
