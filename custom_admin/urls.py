from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import InvestorAdminViewSet, VolunteerAdminViewSet, NewsAdminViewSet, \
	EventAdminViewSet, UserAdminViewSet

router = DefaultRouter()

router.register('user', UserAdminViewSet)
router.register('investor', InvestorAdminViewSet)
router.register('volunteer', VolunteerAdminViewSet)
router.register('news', NewsAdminViewSet)
router.register('event', EventAdminViewSet)

urlpatterns = [
	path('', include(router.urls))
]
