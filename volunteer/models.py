from django.db import models


class News(models.Model):
	images = models.FileField(upload_to='news_content', blank=True, null=True)
	title = models.CharField(max_length=255)
	description = models.TextField()
	address = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)


class Event(models.Model):
	images = models.FileField(upload_to='event_content', blank=True, null=True)
	title = models.CharField(max_length=255)
	description = models.TextField()
	address = models.CharField(max_length=255)
	event_type = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
