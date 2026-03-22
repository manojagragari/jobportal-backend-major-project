from django.conf import settings
from django.db import models


class Job(models.Model):
	EMPLOYMENT_TYPE_CHOICES = [
		("full_time", "Full Time"),
		("part_time", "Part Time"),
		("internship", "Internship"),
		("contract", "Contract"),
	]

	STATUS_CHOICES = [
		("open", "Open"),
		("closed", "Closed"),
	]

	title = models.CharField(max_length=200)
	company_name = models.CharField(max_length=200)
	location = models.CharField(max_length=150, blank=True)
	employment_type = models.CharField(
		max_length=20,
		choices=EMPLOYMENT_TYPE_CHOICES,
		default="full_time",
	)
	description = models.TextField()
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="open")
	created_by = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name="jobs",
	)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return f"{self.title} - {self.company_name}"

	@property
	def is_open(self):
		return self.status == "open"
