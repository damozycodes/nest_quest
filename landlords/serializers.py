from rest_framework import serializers
from .models import Landlord

'''
Serializes the model LandLords
'''
class LandlordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Landlord
        fields = ('user', 'address', 'phone_number')
        