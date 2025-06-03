from rest_framework import viewsets
from rest_framework import permissions

from .models import News, Event
from .serializers import NewsSerializers, EventSerializers


class NewsViewSet(viewsets.ModelViewSet):
	queryset = News.objects.all()
	serializer_class = NewsSerializers
	permission_classes = [permissions.IsAuthenticated]


class EventViewSet(viewsets.ModelViewSet):
	queryset = Event.objects.all()
	serializer_class = EventSerializers
	permission_classes = [permissions.IsAuthenticated]
