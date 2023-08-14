from rest_framework import serializers
from .models import Landlord

'''
Serializes the model LandLords
'''
class PhoneNumberSerializer(serializers.CharField):

    def validate_phone_number(self, Phone_number):
        if len(Phone_number) != 11:
            raise serializers.ValidationError('Phone number must have 11 digits.')

        common_prefixes = ['070', '080', '090', '081', '071', '072', '073', '074', '075', '076', '077', '078', '079']
        if not any(Phone_number.startswith(prefix) for prefix in common_prefixes):
            raise serializers.ValidationError('Invalid phone number.')

        return Phone_number

class LandlordSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberSerializer()

    class Meta:
        model = Landlord
        fields = ('address', 'phone_number')

