from django.db import models
from django.urls import reverse


class Review(models.Model):
	"""
	A review/rating that has been left for a listing
	"""
	listing = models.ForeignKey(
		"listings.Listing",
		on_delete= models.CASCADE,
		related_name= "reviews",
		editable= False,
	)
	reviewer = models.ForeignKey(
		"users.User",
		on_delete= models.CASCADE,
		related_name= "reviews",
		editable= False,
	)
	rating = models.IntegerField(
		"Rating",
		choices= [
			(1, "1 - Very Bad"),
			(2, "2 - Bad"),
			(3, "3 - Okay"),
			(4, "4 - Good"),
			(5, "5 - Very Good"),
		],
	)
	comment = models.CharField(
		"Comment",
		max_length= 511,
	)
	created = models.DateTimeField(auto_now_add= True)
	updated = models.DateTimeField(auto_now= True)

	class Meta:
		unique_together = ("listing", "reviewer")

	def __str__(self):
		return f"<review listing={self.listing.name} reviewer={self.reviewer.email}>"

	def get_absolute_url(self):
		return reverse("reviews:review", kwargs={"pk": self.pk})