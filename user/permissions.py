from rest_framework import permissions


class IsInvestor(permissions.BasePermission):
	def has_permission(self, request, view):
		return hasattr(request.user, 'investor_profile')


class IsVolunteer(permissions.BasePermission):
	def has_permission(self, request, view):
		return hasattr(request.user, 'volunteer_profile')
