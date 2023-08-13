from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import permissions

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