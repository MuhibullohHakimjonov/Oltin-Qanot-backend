from rest_framework import serializers

from payment.models import Order
from user.models import User, Investor, Volunteer
from volunteer.models import Event, News


class UserBaseSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'phone_number']


class InvestorAdminSerializer(serializers.ModelSerializer):
	user = UserBaseSerializer()

	class Meta:
		model = Investor
		fields = ['id', 'user', 'company_name', 'inn', 'address', 'company_owner', 'company_email', 'company_website']


class VolunteerAdminSerializer(serializers.ModelSerializer):
	user = UserBaseSerializer()

	class Meta:
		model = Volunteer
		fields = ['id', 'user', 'name', 'surname', 'date_of_birth', 'address',
				  'gender', 'profile_pic', 'email', 'passport_num']


class EventAdminSerializers(serializers.ModelSerializer):
	class Meta:
		model = Event
		fields = ['id', 'media_content', 'title', 'description', 'address', 'event_type', 'created_at']


class NewsAdminSerializers(serializers.ModelSerializer):
	class Meta:
		model = News
		fields = ['id', 'media_content', 'title', 'description', 'address', 'created_at']


class OrderCreateAdminSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = ['id', 'customer_name', 'address', 'total_cost', 'payment_method', 'is_paid']
