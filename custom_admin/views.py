from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser

from payment.models import Order
from user.models import Volunteer, Investor, User
from volunteer.models import Event, News
from .serializers import VolunteerAdminSerializer, InvestorAdminSerializer, EventAdminSerializers, NewsAdminSerializers, \
	UserBaseSerializer, OrderCreateAdminSerializer


class UserAdminViewSet(ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserBaseSerializer
	permission_classes = [IsAdminUser]


class VolunteerAdminViewSet(ModelViewSet):
	queryset = Volunteer.objects.all()
	serializer_class = VolunteerAdminSerializer
	permission_classes = [IsAdminUser]


class InvestorAdminViewSet(ModelViewSet):
	queryset = Investor.objects.all()
	serializer_class = InvestorAdminSerializer
	permission_classes = [IsAdminUser]


class EventAdminViewSet(ModelViewSet):
	queryset = Event.objects.all()
	serializer_class = EventAdminSerializers
	permission_classes = [IsAdminUser]


class NewsAdminViewSet(ModelViewSet):
	queryset = News.objects.all()
	serializer_class = NewsAdminSerializers
	permission_classes = [IsAdminUser]


class OrderCreateAdminViewSet(ModelViewSet):
	queryset = Order.objects.all()
	serializer_class = OrderCreateAdminSerializer
	permission_classes = [IsAdminUser]
