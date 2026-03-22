from django.contrib import admin

from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
	list_display = ("title", "company_name", "employment_type", "status", "created_by", "created_at")
	list_filter = ("status", "employment_type", "created_at")
	search_fields = ("title", "company_name", "location", "description")
