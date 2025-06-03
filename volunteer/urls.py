from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, NewsViewSet

router = DefaultRouter()

router.register('news', NewsViewSet)
router.register('events', EventViewSet)

urlpatterns = [
	path('', include(router.urls))
]
