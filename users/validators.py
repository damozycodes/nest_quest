from django.contrib.auth.validators import UnicodeUsernameValidator, _


class NameValidator(UnicodeUsernameValidator):
	regex = r"^[\w]{3,150}\Z"
	message = _(
		"The name must be between 3 and 150 character and may contain letters."
	)