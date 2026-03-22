from django.contrib import admin

from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
	list_display = ("job", "applicant", "status", "email", "created_at")
	list_filter = ("status", "created_at")
	search_fields = ("job__title", "applicant__username", "full_name", "email")
