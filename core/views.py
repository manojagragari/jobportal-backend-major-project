from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import JobForm
from .models import Job


def home(request):
    featured_jobs = Job.objects.filter(status="open")[:6]
    return render(request, "core/home.html", {"featured_jobs": featured_jobs})


def jobs(request):
    query = request.GET.get("q", "").strip()
    jobs_qs = Job.objects.all()
    if query:
        jobs_qs = jobs_qs.filter(
            Q(title__icontains=query)
            | Q(company_name__icontains=query)
            | Q(location__icontains=query)
            | Q(employment_type__icontains=query)
        )

    return render(
        request,
        "core/jobs.html",
        {
            "jobs": jobs_qs,
            "query": query,
        },
    )


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    already_applied = False

    if request.user.is_authenticated:
        already_applied = job.applications.filter(applicant=request.user).exists()

    return render(
        request,
        "core/job_detail.html",
        {"job": job, "already_applied": already_applied},
    )


@login_required
@user_passes_test(lambda user: user.is_staff)
def create_job(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            job.save()
            messages.success(request, "Job posted successfully.")
            return redirect("core:job_detail", pk=job.pk)
    else:
        form = JobForm()

    return render(request, "core/job_form.html", {"form": form})

