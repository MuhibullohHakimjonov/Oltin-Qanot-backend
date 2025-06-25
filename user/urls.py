from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
	TokenObtainPairView,
	TokenRefreshView,
)
from .views import (
	RequestCodeView,
	ConfirmCodeView,
	InvestorRegisterView,
	VolunteerRegisterView, InvestorProfileView, VolunteerProfileView, MeProfileView
)

urlpatterns = [
	path('send/code/', RequestCodeView.as_view(), name='send_code'),
	path('verify/code/', ConfirmCodeView.as_view(), name='verify_code'),
	path('register/investor/', InvestorRegisterView.as_view(), name='register_investor'),
	path('register/volunteer/', VolunteerRegisterView.as_view(), name='register_volunteer'),
	path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

	path('investors/<int:pk>/', InvestorProfileView.as_view(), name='investor-profile'),
	path('volunteers/<int:pk>/', VolunteerProfileView.as_view(), name='volunteer-profile'),
	path('me/', MeProfileView.as_view(), name='me-profile'),
]
