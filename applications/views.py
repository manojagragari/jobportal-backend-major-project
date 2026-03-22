from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from core.models import Job

from .forms import ApplicationForm


@login_required
def apply(request, id):
    job = get_object_or_404(Job, id=id)

    if not job.is_open:
        messages.error(request, "This job is currently closed.")
        return redirect("core:job_detail", pk=job.pk)

    if job.applications.filter(applicant=request.user).exists():
        messages.info(request, "You have already applied to this job.")
        return redirect("core:job_detail", pk=job.pk)

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, "Application submitted successfully.")
            return redirect("users:dashboard")
    else:
        form = ApplicationForm(
            initial={
                "full_name": request.user.get_full_name() or request.user.username,
                "email": request.user.email,
            }
        )

    return render(request, "applications/apply.html", {"form": form, "job": job})
