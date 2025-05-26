from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.password_validation import validate_password

from .models import User, Investor, Volunteer, PhoneVerification


class PhoneVerificationSerializer(serializers.Serializer):
	phone_number = serializers.CharField()


class CodeVerificationSerializer(serializers.Serializer):
	phone_number = serializers.CharField()
	code = serializers.CharField(max_length=6)


class InvestorRegisterSerializer(serializers.ModelSerializer):
	phone_number = serializers.CharField()
	password = serializers.CharField(write_only=True, validators=[validate_password])
	confirm_password = serializers.CharField(write_only=True)

	class Meta:
		model = Investor
		fields = ['phone_number', 'password', 'confirm_password', 'company_name', 'inn', 'address']

	def validate(self, data):
		if data['password'] != data['confirm_password']:
			raise serializers.ValidationError({"confirm_password": "Passwords must match"})

		phone = data['phone_number'].replace('+', '')
		try:
			pv = PhoneVerification.objects.get(phone_number=phone)
			if not pv.is_verified or pv.created_at < timezone.now() - timedelta(minutes=5):
				raise serializers.ValidationError({"phone_number": "Phone number is not verified or code expired"})
		except PhoneVerification.DoesNotExist:
			raise serializers.ValidationError({"phone_number": "Phone number is not verified"})

		return data

	def create(self, validated_data):
		phone = validated_data.pop('phone_number').replace('+', '')
		password = validated_data.pop('password')
		validated_data.pop('confirm_password')

		user = User.objects.create_user(phone_number=phone, password=password)
		investor = Investor.objects.create(user=user, **validated_data)

		PhoneVerification.objects.filter(phone_number=phone).delete()  # Очистить верификацию после успешной регистрации

		return investor


class VolunteerRegisterSerializer(serializers.ModelSerializer):
	phone_number = serializers.CharField()
	password = serializers.CharField(write_only=True, validators=[validate_password])
	confirm_password = serializers.CharField(write_only=True)

	class Meta:
		model = Volunteer
		fields = ['phone_number', 'password', 'confirm_password', 'name', 'surname', 'date_of_birth', 'address',
				  'gender']

	def validate(self, data):
		if data['password'] != data['confirm_password']:
			raise serializers.ValidationError({"confirm_password": "Passwords must match"})

		phone = data['phone_number'].replace('+', '')
		try:
			pv = PhoneVerification.objects.get(phone_number=phone)
			if not pv.is_verified or pv.created_at < timezone.now() - timedelta(minutes=5):
				raise serializers.ValidationError({"phone_number": "Phone number is not verified or code expired"})
		except PhoneVerification.DoesNotExist:
			raise serializers.ValidationError({"phone_number": "Phone number is not verified"})

		return data

	def create(self, validated_data):
		phone = validated_data.pop('phone_number').replace('+', '')
		password = validated_data.pop('password')
		validated_data.pop('confirm_password')

		user = User.objects.create_user(phone_number=phone, password=password)
		volunteer = Volunteer.objects.create(user=user, **validated_data)

		PhoneVerification.objects.filter(phone_number=phone).delete()

		return volunteer


class UserBaseSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'phone_number']


class InvestorSerializer(serializers.ModelSerializer):
	user = UserBaseSerializer()

	class Meta:
		model = Investor
		fields = ['id', 'user', 'company_name', 'inn', 'address', 'company_owner', 'company_email', 'company_website']

	def update(self, instance, validated_data):
		user_data = validated_data.pop('user', {})
		if 'phone_number' in user_data:
			instance.user.phone_number = user_data['phone_number']
			instance.user.save()

		for attr, value in validated_data.items():
			setattr(instance, attr, value)
		instance.save()
		return instance


class VolunteerSerializer(serializers.ModelSerializer):
	user = UserBaseSerializer()

	class Meta:
		model = Volunteer
		fields = ['id', 'user', 'name', 'surname', 'date_of_birth', 'address',
				  'gender', 'profile_pic', 'email', 'passport_num']

	def update(self, instance, validated_data):
		user_data = validated_data.pop('user', {})
		if 'phone_number' in user_data:
			instance.user.phone_number = user_data['phone_number']
			instance.user.save()

		for attr, value in validated_data.items():
			setattr(instance, attr, value)
		instance.save()
		return instance
