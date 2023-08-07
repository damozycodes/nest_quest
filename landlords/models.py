from django.db import models
from users.models import User
from django.db import models
from django.core.validators import RegexValidator


class Landlord(models.Model):
    phoneRex = RegexValidator(
        regex=r'^\d{11}$',
        message='Phone number must be entered in the format: "070xxxxxxxx". 11 digits allowed.'
    )
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    phone_number = models.CharField(validators=[phoneRex],max_length=11)

    def __str__(self):
        return f"<landlord email={self.email}>"

