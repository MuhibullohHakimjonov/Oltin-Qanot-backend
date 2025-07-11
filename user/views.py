from django.core.cache import cache
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Volunteer, Investor
from .serializers import (
	PhoneVerificationSerializer,
	CodeVerificationSerializer,
	InvestorRegisterSerializer,
	VolunteerRegisterSerializer, InvestorSerializer, VolunteerSerializer, MeProfileUpdateSerializer
)
from .services import send_verification_sms, verify_code


class RequestCodeView(APIView):
	def post(self, request):
		serializer = PhoneVerificationSerializer(data=request.data)
		if serializer.is_valid():
			phone = serializer.validated_data['phone_number']
			if send_verification_sms(phone):
				return Response({"detail": "Code sent"}, status=status.HTTP_200_OK)
			return Response({"error": "Failed to send SMS"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmCodeView(APIView):
	def post(self, request):
		serializer = CodeVerificationSerializer(data=request.data)
		if serializer.is_valid():
			phone = serializer.validated_data['phone_number'].replace('+', '')
			code = serializer.validated_data['code']

			if verify_code(phone, code):
				cache.set(f"verified_{phone}", True, timeout=300)
				return Response({"message": "Phone number verified successfully"}, status=200)
			return Response({"error": "Invalid or expired code"}, status=400)
		return Response(serializer.errors, status=400)


class InvestorRegisterView(APIView):
	def post(self, request):
		serializer = InvestorRegisterSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({"detail": "Investor registered"}, status=201)
		return Response(serializer.errors, status=400)


class VolunteerRegisterView(APIView):
	def post(self, request):
		serializer = VolunteerRegisterSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({"detail": "Volunteer registered"}, status=201)
		return Response(serializer.errors, status=400)


class InvestorProfileView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request, pk=None):
		if pk is None:
			investors = Investor.objects.all()
			serializer = InvestorSerializer(investors, many=True)
			return Response(serializer.data)

		investor = get_object_or_404(Investor, pk=pk)
		serializer = InvestorSerializer(investor)
		return Response(serializer.data)

	def put(self, request, pk):
		investor = get_object_or_404(Investor, pk=pk)

		if request.user != investor.user and not request.user.is_staff:
			return Response({'detail': 'You do not have permission to edit this profile.'}, status=403)

		serializer = InvestorSerializer(investor, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VolunteerProfileView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request, pk=None):
		if pk is None:
			volunteers = Volunteer.objects.all()
			serializer = VolunteerSerializer(volunteers, many=True)
			return Response(serializer.data)

		volunteer = get_object_or_404(Volunteer, pk=pk)
		serializer = VolunteerSerializer(volunteer)
		return Response(serializer.data)

	def put(self, request, pk):
		volunteer = get_object_or_404(Volunteer, pk=pk)

		if request.user != volunteer.user and not request.user.is_staff:
			return Response({'detail': 'You do not have permission to edit this profile.'}, status=403)

		serializer = VolunteerSerializer(volunteer, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeProfileView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		user = request.user

		investor = Investor.objects.select_related('user').filter(user=user).first()
		volunteer = Volunteer.objects.select_related('user').filter(user=user).first()

		if not investor and not volunteer:
			return Response({'detail': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)

		role = 'investor' if investor else 'volunteer'

		investor_data = InvestorSerializer(investor).data if investor else {
			"id": None,
			"user": {"id": user.id, "phone_number": user.phone_number},
			"company_name": None,
			"inn": None,
			"address": None,
			"company_owner": None,
			"company_email": None,
			"company_website": None
		}

		volunteer_data = VolunteerSerializer(volunteer).data if volunteer else {
			"name": None,
			"surname": None,
			"date_of_birth": None,
			"address": None,
			"gender": None,
			"profile_pic": None,
			"email": None,
			"passport_num": None
		}

		merged_profile = {
			**investor_data,
			**{k: v for k, v in volunteer_data.items() if k != 'user'}
		}

		return Response({
			'role': role,
			'profile': merged_profile
		})

	@extend_schema(
		request=MeProfileUpdateSerializer,
		responses={200: MeProfileUpdateSerializer},
	)
	def put(self, request):
		user = request.user

		investor = Investor.objects.filter(user=user).first()
		volunteer = Volunteer.objects.filter(user=user).first()

		if not investor and not volunteer:
			return Response({'detail': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)

		updated_data = {}

		if investor:
			serializer = InvestorSerializer(investor, data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				updated_data.update(serializer.data)
			else:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		if volunteer:
			serializer = VolunteerSerializer(volunteer, data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				updated_data.update(serializer.data)
			else:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		return Response({'detail': 'Profile updated successfully', 'profile': updated_data})
