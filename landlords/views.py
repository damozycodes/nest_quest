from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Landlord
from .serializers import LandlordSerializer
from rest_framework import generics

# extra parameters to be passed through post

class CreateLandlordView(generics.CreateAPIView):
    serializer_class = LandlordSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LandlordInfoView(generics.RetrieveUpdateAPIView):
    serializer_class = LandlordSerializer

    def get_object(self):
        return get_object_or_404(Landlord, user=self.request.user)

