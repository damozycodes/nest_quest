from typing import TypedDict
from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from landlords.models import Landlord
from .models import Listing
from .permissions import IsLandlord, IsOwnerOrReadOnly
from .serializers import ListingSerializer
from rest_framework.pagination import LimitOffsetPagination


class NewListingView(generics.CreateAPIView):
	"""
	Create a new listing, requires authentication as a landlord
	"""
	permission_classes = [permissions.IsAuthenticated, IsLandlord]
	serializer_class = ListingSerializer

	def perform_create(self, serializer):
		serializer.save(landlord= self.request.user.landlord)


class ListingView(generics.RetrieveUpdateDestroyAPIView):
	"""
	Get or update a listing
	"""
	permission_classes = [IsOwnerOrReadOnly]
	queryset = Listing.objects.all()
	serializer_class = ListingSerializer


class ListListingView(generics.ListAPIView):
	"""
	Get all of a landlord's listing
	"""
	permission_classes = [permissions.AllowAny]
	serializer_class = ListingSerializer
	pagination_class = LimitOffsetPagination

	def get_queryset(self):
		landlord = get_object_or_404(Landlord, pk= self.kwargs.get("pk"))
		return Listing.objects.filter(landlord= landlord)


class SearchSchema(TypedDict):
	rent_min: int | None
	rent_max: int | None
	types_allowed: str | None
	created_min: datetime | None
	created_max: datetime | None
	updated_min: datetime | None
	updated_max: datetime | None
	sort: str | None
	reverse: str | None


class SearchListingView(generics.ListAPIView):
	"""
	Search for listings
	"""
	permission_classes = [permissions.AllowAny]
	serializer_class = ListingSerializer

	def get_queryset(self):
		queryset = Listing.objects.all()
		data: SearchSchema = self.request.query_params

		if data.get("rent_min") is not None:
			queryset = queryset.filter(rent__gte= data["rent_min"])
		if data.get("rent_max") is not None:
			queryset = queryset.filter(rent__lte= data["rent_max"])
		if data.get("types_allowed") is not None:
			queryset = queryset.filter(type__in= data["types_allowed"].split(","))
		if data.get("created_min") is not None:
			queryset = queryset.filter(created__gte= data["created_min"])
		if data.get("created_max") is not None:
			queryset = queryset.filter(created__lte= data["created_max"])
		if data.get("updated_min") is not None:
			queryset = queryset.filter(updated__gte= data["updated_min"])
		if data.get("updated_max") is not None:
			queryset = queryset.filter(updated__lte= data["updated_max"])
		if data.get("sort") in ("rent", "created", "updated"):
			queryset = queryset.order_by(data["sort"])
		if data.get("reverse") in ("true", "True", "1", "yes", "Yes"):
			queryset = queryset.reverse()
			
		return queryset


class LikeListingView(APIView):
	"""
	Like or unlike a listing
	"""
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request, *args, **kwargs):
		listing = get_object_or_404(Listing, pk= kwargs.get("pk"))
		if request.user == listing.landlord.user:
			return Response(status= status.HTTP_403_FORBIDDEN, data= {
				"detail": "You cannot like your own listing",
			})
		
		if request.user in listing.likes.all():
			listing.likes.remove(request.user)
			action = "unliked"
		else:
			listing.likes.add(request.user)
			action = "liked"
		
		listing.save()
		return Response(status= status.HTTP_200_OK, data= {
			"detail": f"You have {action} this listing",
		})