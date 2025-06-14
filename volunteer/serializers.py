from rest_framework import serializers
from .models import Event, News


class EventSerializers(serializers.ModelSerializer):
	class Meta:
		model = Event
		fields = ['id', 'media_content', 'title', 'description', 'address', 'event_type', 'created_at']


class NewsSerializers(serializers.ModelSerializer):
	class Meta:
		model = News
		fields = ['id', 'media_content', 'title', 'description', 'address', 'created_at']
