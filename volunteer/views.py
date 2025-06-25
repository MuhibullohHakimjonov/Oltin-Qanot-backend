from rest_framework import viewsets
from rest_framework import permissions
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import News, Event
from .serializers import NewsSerializers, EventSerializers



@extend_schema(
    parameters=[OpenApiParameter(name='event_type', description='Тип события', required=False, type=str),
	OpenApiParameter(name='address', description='Адрес события', required=False, type=str),])
class NewsViewSet(viewsets.ModelViewSet):
	queryset = News.objects.all()
	serializer_class = NewsSerializers
	permission_classes = [permissions.IsAuthenticated]


class EventViewSet(viewsets.ModelViewSet):
	queryset = Event.objects.all()
	serializer_class = EventSerializers
	permission_classes = [permissions.IsAuthenticated]
