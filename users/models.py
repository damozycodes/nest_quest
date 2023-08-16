import uuid

from django.contrib.auth.models import AbstractUser, _
from django.db import models
from django.urls import reverse

from users import validators
from cloudinary.models import CloudinaryField
from cloudinary import utils as cloudinary_utils


class User(AbstractUser):
	name_validator = validators.NameValidator()

	id = models.UUIDField(primary_key= True, default= uuid.uuid4, editable= False)

	email = models.EmailField(
		_("email address"),
		unique= True,
		error_messages= {
			"unique": _("That email address is already in use"),
		},
	)

	# username field isn't used, but is here so we don't break things
	username = models.CharField(
		_("username"),
		max_length=150,
		validators= [name_validator],
	)

	first_name = models.CharField(
		_("first name"),
		max_length=150,
		validators= [name_validator],
	)

	last_name = models.CharField(
		_("last name"),
		max_length=150,
		validators= [name_validator],
	)

	default_profile_picture_url = 'media/profile_picture/profile_picture.png'

	profile_picture = CloudinaryField(
		resource_type='image',
		default=default_profile_picture_url,
		blank=True,
		null=True
	)

	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ["username"]


	def is_landlord(self):
		return hasattr(self, "landlord")

	def get_absolute_url(self):
		return reverse("user", kwargs={"pk": self.pk})

	def get_secure_profile_picture_url(self):
		if self.profile_picture:
			url, options = cloudinary_utils.cloudinary_url(self.profile_picture.public_id, secure=True)
			return url
		return None