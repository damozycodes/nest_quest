from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Listing


class ListingSerializer(ModelSerializer):
	rating = serializers.DecimalField(max_digits=3, decimal_places=1)
	class Meta:
		model = Listing
		fields = "__all__"