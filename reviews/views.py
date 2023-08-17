from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import permissions

from listings.models import Listing
from .models import Review
from .permissions import IsOwnerOrReadOnly
from .serializers import ReviewSerializer


class NewReviewView(generics.CreateAPIView):
	"""
	Create a new review, requires authentication as a user

	"""
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = ReviewSerializer

	def perform_create(self, serializer):
		review = get_object_or_404(Listing, pk= self.kwargs.get("pk"))
		if review.landlord == self.request.user:
			"""check if the user is same as the landlord who made the list"""
			raise ReviewSerializer.ValidationError(
				{"reviewer": "You cannot review your own listing."}
			)
		serializer.save(
			reviewer= self.request.user,
			listing= get_object_or_404(Listing, pk= self.kwargs.get("pk")),
		)


class ReviewView(generics.RetrieveUpdateDestroyAPIView):
	"""
	Get/update/delete a review
	"""
	permission_classes = [IsOwnerOrReadOnly]
	queryset = Review.objects.all()
	serializer_class = ReviewSerializer


class ListingReviewView(generics.ListAPIView):
	"""
	Get all reviews of a listing
	"""
	permission_classes = [permissions.AllowAny]
	queryset = Review.objects.all()
	serializer_class = ReviewSerializer

	def get_queryset(self):
		listing = get_object_or_404(Listing, pk= self.kwargs.get("pk"))
		return Review.objects.filter(listing= listing)


class UserReviewView(generics.ListAPIView):
	"""
	Get all reviews of a user. Requires authentication as that user.
	"""
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = ReviewSerializer

	def get_queryset(self):
		return Review.objects.filter(reviewer= self.request.user)