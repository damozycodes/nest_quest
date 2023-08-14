from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Review
from listings.models import Listing
from django.db import models

@receiver(post_save, sender=Review)
@receiver(pre_delete, sender=Review)
def update_listing_rating(sender, instance, **kwargs):
    print("nest Signal triggered!......")
    listing = instance.listing

    reviews = listing.reviews.all()
    total_ratings = reviews.count()
    sum_ratings = reviews.aggregate(models.Sum('rating'))['rating__sum']

    if sum_ratings is not None:
        listing.sum_ratings = sum_ratings
        listing.total_ratings = total_ratings
        listing.save()
