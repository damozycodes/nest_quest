from rest_framework.serializers import ModelSerializer

from .models import MatchingRequest


class MatchingRequestSerializer(ModelSerializer):
    class Meta:
        model = MatchingRequest
        fields = '__all__'
        read_only_fields = ["id", "created_at", "updated_at", "user", ]