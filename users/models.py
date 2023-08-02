import uuid

from django.contrib.auth.models import AbstractUser, _
from django.db import models

from users import validators 


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

	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ["username"]