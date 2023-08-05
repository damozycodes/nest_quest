from django.db import models
from users.models import User
from django.db import models


class Landlord(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"<landlord email={self.email}>"
