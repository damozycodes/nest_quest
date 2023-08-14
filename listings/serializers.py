from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Listing


class ListingSerializer(ModelSerializer):
	likes = SerializerMethodField()
	is_liked = SerializerMethodField()

	def get_likes(self, obj):
		return obj.likes.count()
	
	def get_is_liked(self, obj):
		return self.context["request"].user in obj.likes.all()
	
	class Meta:
		model = Listing
		fields = "__all__"
		read_only_fields = ["landlord", "likes", "created", "updated", "is_liked"]