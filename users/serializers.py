from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    profile_picture_url = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('pk', 'email', 'first_name', 'last_name', 'profile_picture','profile_picture_url')

    def get_profile_picture_url(self, obj):
        return obj.get_secure_profile_picture_url()
