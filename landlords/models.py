from django.db import models
from users.models import User
from django.db import models
from django.core.validators import RegexValidator


class Landlord(models.Model):
    phoneRex = RegexValidator(
        regex=r'^0[7-9][0-1]\d{8}$',
        message='Phone number must be entered in the format: "070, 071, 080, 081, 090, 091". 11 digits allowed.'
    )
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    phone_number = models.CharField(
        max_length=11,
		validators=[phoneRex],
    )

    def __str__(self):
        return f"<landlord email={self.user.email}>"

