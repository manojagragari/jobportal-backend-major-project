from django.conf import settings
from django.db import models


class Application(models.Model):
	STATUS_CHOICES = [
		("submitted", "Submitted"),
		("reviewed", "Reviewed"),
		("shortlisted", "Shortlisted"),
		("rejected", "Rejected"),
	]

	job = models.ForeignKey("core.Job", on_delete=models.CASCADE, related_name="applications")
	applicant = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name="applications",
	)
	full_name = models.CharField(max_length=150)
	email = models.EmailField()
	cv = models.FileField(upload_to="cvs/")
	cover_letter = models.TextField(blank=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="submitted")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-created_at"]
		constraints = [
			models.UniqueConstraint(fields=["job", "applicant"], name="unique_job_applicant")
		]

	def __str__(self):
		return f"{self.applicant.username} -> {self.job.title}"
