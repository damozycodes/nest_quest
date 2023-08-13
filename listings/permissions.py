from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsLandlord(BasePermission):
	"""
	Allows access only to landlords.
	"""
	def has_permission(self, request, view):
		return request.user.is_landlord()


class IsOwnerOrReadOnly(BasePermission):
	"""
	Allows write access only to landlords of the listing.
	"""
	def has_object_permission(self, request, view, obj):
		if request.method in SAFE_METHODS:
			return True
		return request.user and request.user.is_authenticated \
			and request.user.is_landlord() and obj.landlord == request.user.landlord