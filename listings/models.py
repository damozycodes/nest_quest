import uuid

from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class Listing(models.Model):
	"""
	A model that represents a listing

	TODO: location, distance_to_gate, utilities, is_availaible, is_active
	"""
	MINIMUM_PRICE = 10000

	SINGLE_ROOM = "SINGLE_ROOM"
	SELF_CON = "SELF_CON"
	ONE_BEDROOM_FLAT = "ONE_BEDROOM_FLAT"
	TWO_BEDROOMS_FLAT = "TWO_BEDROOMS_FLAT"
	THREE_BEDROOMS_FLAT = "THREE_BEDROOMS_FLAT"
	FOUR_BEDROOMS_FLAT = "FOUR_BEDROOMS_FLAT"
	TYPES = [
		(SINGLE_ROOM, "Single Room"),
		(SELF_CON, "Self Contained"),
		(ONE_BEDROOM_FLAT, "One Bedroom Flat"),
		(TWO_BEDROOMS_FLAT, "Two Bedrooms Flat"),
		(THREE_BEDROOMS_FLAT, "Three Bedrooms Flat"),
		(FOUR_BEDROOMS_FLAT, "Four Bedrooms Flat"),
	]

	id = models.UUIDField(primary_key= True, default= uuid.uuid4)
	name = models.CharField(max_length= 255)
	description = models.TextField(
		"Detailed description of the listing",
	)
	rent = models.IntegerField(
		"Rent per year",
		validators= [MinValueValidator(
			MINIMUM_PRICE,
			f"Rent must be at least {MINIMUM_PRICE}",
		)],
	)
	address = models.CharField(
		"Address of the listing",
		max_length= 255,
		unique= True,
	)
	type = models.CharField(
		"Type of listing",
		max_length= 255,
		choices= TYPES,
	)
	landlord = models.ForeignKey(
		"landlords.Landlord",
		on_delete= models.CASCADE,
		related_name= "listings",
		editable= False,
	)
	likes = models.ManyToManyField(
		"users.User",
		related_name= "liked_listings",
		verbose_name= "Users who have liked this listing",
	)
	created = models.DateTimeField(auto_now_add= True)
	updated = models.DateTimeField(auto_now= True)

	class Meta:
		ordering = ["-updated", "-created"]

	def __str__(self):
		return self.name
	
	def get_absolute_url(self):
		return reverse("listings:listing", kwargs= {"pk": self.pk})