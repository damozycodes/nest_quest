"""
Tests for the auth views
"""

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from users.models import User


class AuthViewsTestCase(APITestCase):
    def test_signup(self):
        """
        Test that we can signup
        """
        url = reverse("signup")
        data = {
            "email": "mail@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, "mail@example.com")


    def test_user(self):
        """
        Test that we can get user details
        """
        url = reverse("user")
        user = User.objects.create_user(
            email= "mail@example.com",
            password= "testpassword",
            username = "username",
            first_name = "Suzy",
            last_name = "Smith",
        )
        client = APIClient()
        client.force_authenticate(user= user)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "mail@example.com")
        self.assertEqual(response.data["first_name"], "Suzy")
        self.assertEqual(response.data["last_name"], "Smith")


    def test_login(self):
        """
        Test that we can login
        """
        url = reverse("login")
        user = User.objects.create_user(
            email= "mail@example.com",
            password= "testpassword",
            username = "username",
        )
        data = {
            "email": "mail@example.com",
            "password": "testpassword",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_logout(self):
        """
        Test that we can logout
        """
        url = reverse("logout")
        user = User.objects.create_user(
            email= "mail@example.com",
            password= "testpassword",
            username = "username",
        )
        client = APIClient()
        client.force_authenticate(user= user)
        response = client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_change_password(self):
        """
        Test that we can change our password
        """
        url = reverse("change_password")
        user = User.objects.create_user(
            email= "mail@example.com",
            password= "testpassword",
            username = "username",
        )
        client = APIClient()
        client.force_authenticate(user= user)
        data = {
            "new_password1": "uncommontestpassword852147",
            "new_password2": "uncommontestpassword852147",
        }
        response = client.post(url, data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_account_confirm_email(self):
        """
        Test that we can confirm our email
        TODO: figure out how to test this
        """
        pass