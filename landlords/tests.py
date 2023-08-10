from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from .models import Landlord
from .serializers import LandlordSerializer, PhoneNumberSerializer

class LandlordTests(APITestCase):
    
    def setUp(self):
        # test to create a user
        self.user = User.objects.create(username='user1', email='@12fasdlkjh')
        self.client.force_authenticate(user=self.user)

    def test_create(self):
        url = reverse("create_landlord")
        data = {
            "user": self.user.id,
            "phone_number": "080123456789",
            "address": "address",
        }
        response = self.client.post(url, data)
        self.assertEqual(Landlord.objects.count(), 1)
        self.assertEqual(Landlord.objects.get().address, "address")
        self.assertEqual(Landlord.objects.get().phone_number, "080123456789")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_get_landlord(self):
        landlord = Landlord.objects.create(
            user = self.user,
            phone_number = "07062617961",
            address = "oau",
            )
        url = reverse("landlord_info")
        response = self.client.get(url)
        serializer = LandlordSerializer(landlord)
        self.assertEqual(response.data,serializer.data)

    def test_update_landlord(self):
        url = reverse("landlord_info")
        landlord = Landlord.objects.create(
            user = self.user,
            phone_number = "07062617961",
            address = "oau",
        )
        data = {
            "address": "new address",
            "phone_number": "080123456789",
        }
        response = self.client.patch(url, data)
        self.assertEqual(Landlord.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Landlord.objects.get().address, "new address")
        self.assertEqual(Landlord.objects.get().phone_number, "080123456789")


    def test_validate_phone_number(self):
        phone_number = '08012345678'
        validated_phone_number = PhoneNumberSerializer().validate_phone_number(phone_number)
        self.assertEqual(validated_phone_number, phone_number)