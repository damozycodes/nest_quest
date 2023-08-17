from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import MatchingRequest
from .permissions import IsOwnerOrReadOnly
from .serializers import MatchingRequestSerializer


class NewMatchingRequestView(generics.CreateAPIView):
	"""
	Create a new matching request
	"""
	serializer_class = MatchingRequestSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)


class MatchingRequestView(generics.RetrieveUpdateDestroyAPIView):
	"""
	Retrieve, update or delete a matching request
	"""
	queryset = MatchingRequest.objects.all()
	serializer_class = MatchingRequestSerializer
	permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

	def get_object(self):
		return self.request.user.matching_request
	

class GetMatchingsView(generics.ListAPIView):
	"""
	Fetch similar matching requests
	"""
	serializer_class = MatchingRequestSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		matching_request = get_object_or_404(MatchingRequest, user= self.request.user)
		return matching_request.get_similar_matchings_queryset()