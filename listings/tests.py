"""
Tests for the listings app
"""

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from listings.models import Listing


class ListingViewsTestCase(APITestCase):
    pass