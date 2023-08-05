from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Landlord
from .serializers import LandlordSerializer

# extra parameters to be passed through post

@api_view(['POST'])
def create_landlord(request):
    serializer = LandlordSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH'])
def landlord_info(request):
    landlord = get_object_or_404(Landlord, user=request.user)
    
    if request.method == 'GET':
        serializer = LandlordSerializer(landlord)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = LandlordSerializer(landlord, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

