from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Case, F, IntegerField, Q, When
from django.db.models.functions import Abs


class MatchingRequest(models.Model):
	"""
	A request to match a user with a partner
	"""
	phoneregex = RegexValidator(regex=r'^0[7-9][0-1]\d{8}$')

	CHRISTIANITY = "CHRISTIANITY"
	ISLAM = "ISLAM"
	TRADITIONAL = "TRADITIONAL"
	OTHER = "OTHER"
	RELIGIONS = [
		(CHRISTIANITY, "Christianity"),
		(ISLAM, "Islam"),
		(TRADITIONAL, "Traditional"),
		(OTHER, "Other"),
	]

	ADMINISTRATION = "ADMINISTRATION"
	AGRICULTURE = "AGRICULTURE"
	ARTS = "ARTS"
	EDM = "EDM"
	EDUCATION = "EDUCATION"
	HEALTH = "HEALTH"
	LAW = "LAW"
	SCIENCE = "SCIENCE"
	SOCIAL_SCIENCE = "SOCIAL SCIENCE"
	TECHNOLOGY = "TECHNOLOGY"
	FACULTIES = [
		(ADMINISTRATION, "Administration"),
		(AGRICULTURE, "Agriculture"),
		(ARTS, "Arts"),
		(EDM, "Enviromental Design and Management"),
		(EDUCATION, "Education"),
		(HEALTH, "Health"),
		(LAW, "Law"),
		(SCIENCE, "Science"),
		(SOCIAL_SCIENCE, "Social Science"),
		(TECHNOLOGY, "Technology"),
	]

	user = models.OneToOneField(
		"users.User",
		on_delete=models.CASCADE,
		related_name='matching_request',
	)
	phone_number = models.CharField(max_length= 11, validators= [phoneregex])
	description = models.TextField(default= "No additional description was provided.")

	own_age = models.IntegerField()
	min_age = models.IntegerField()
	max_age = models.IntegerField()

	budget_min = models.IntegerField()
	budget_max = models.IntegerField()
	room_types = models.CharField(
		"Types of listing you're looking for",
		max_length= 255,
	)

	own_religion = models.CharField(
		"Religion",
		max_length= 255,
		choices= RELIGIONS,
	)
	preferred_religions = models.CharField(
		"Preferred religions",
		max_length= 255,
		default= "",
	)
	unwanted_religions = models.CharField(
		"Unwanted religions",
		max_length= 255,
		default= "",
	)

	own_faculty = models.CharField(
		"Faculty",
		max_length= 255,
		choices= FACULTIES,
	)
	preferred_faculties = models.CharField(
		"Preferred faculties",
		max_length= 255,
		default= "",
	)
	unwanted_faculties = models.CharField(
		"Unwanted faculties",
		max_length= 255,
		default= "",
	)

	created_at = models.DateTimeField(auto_now_add= True)
	updated_at = models.DateTimeField(auto_now= True)

	def get_similar_matchings_queryset(self):
		"""
		Filter and return a queryset sorted by similarity
		"""
		queryset = MatchingRequest.objects.exclude(user= self.user)

		# filter age, budget, religion and faculty
		queryset = queryset.filter(
			own_age__gte= self.min_age,
			own_age__lte= self.max_age,
			min_age__lte= self.own_age,
			max_age__gte= self.own_age,
			budget_max__gte= self.budget_min,
			budget_min__lte= self.budget_max,
		).exclude(
			own_religion__in= self.unwanted_religions.split(','),
			own_faculty__in= self.unwanted_faculties.split(','),
			unwanted_religions__contains= self.own_religion,
			unwanted_faculties__contains= self.own_faculty,
	    )

		# filter room types
		room_types = self.room_types.split(',')
		q = Q(room_types__contains= room_types[0])
		for room_type in room_types[1:]:
			q |= Q(room_types__contains=room_type)
		queryset = queryset.filter(q)

		# annotate similarity metrics
		budget_avg =  (self.budget_min + self.budget_max) / 2
		queryset = queryset.annotate(
			age_diff= Abs(F('own_age') - self.own_age),
			budget_diff= Abs(
				(F('budget_min') + F("budget_max")) / 2 - budget_avg
			),
			age_score = Case(
				When(age_diff__lte=1, then=1),
				When(age_diff__lte=2, then=0.8),
				When(age_diff__lte=3, then=0.6),
				When(age_diff__lte=4, then=0.4),
				When(age_diff__lte=5, then=0.2),
				default=0,
				output_field=IntegerField(),
			),
			budget_score = Case(
				When(budget_diff__lte=10000, then=1),
				When(budget_diff__lte=20000, then=0.8),
				When(budget_diff__lte=30000, then=0.6),
				When(budget_diff__lte=40000, then=0.4),
				When(budget_diff__lte=50000, then=0.2),
				default=0,
				output_field=IntegerField(),
			),
			same_religion= Case(
				When(own_religion=self.unwanted_religions, then=0.5),
				default=0,
				output_field=IntegerField(),
			),
			same_faculty= Case(
				When(own_faculty=self.unwanted_faculties, then=0.5),
				default=0,
				output_field=IntegerField(),
			),
			own_religion_preferred= Case(
				When(preferred_religions__contains=self.own_religion, then=1),
				default=0,
				output_field=IntegerField(),
			),
			own_faculty_preferred= Case(
				When(preferred_faculties__contains=self.own_faculty, then=1),
				default=0,
				output_field=IntegerField(),
			),
			other_religion_preferred= Case(
				When(own_religion__in= self.preferred_religions, then=1),
				default=0,
				output_field=IntegerField(),
			),
			other_faculty_preferred= Case(
				When(own_faculty__in= self.preferred_faculties, then=1),
				default=0,
				output_field=IntegerField(),
			),
		)

		# sort by total score
		queryset = queryset.annotate(
			total_score= sum([
				F("age_score"),
				F("budget_score"),
				F("same_religion"),
				F("same_faculty"),
				F("own_religion_preferred"),
				F("own_faculty_preferred"),
				F("other_religion_preferred"),
				F("other_faculty_preferred"),
			])
		).order_by("-total_score")

		return queryset