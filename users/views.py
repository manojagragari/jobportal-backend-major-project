from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from .forms import LoginForm, RegisterForm, ProfileForm
from .models import Profile


def register(request):
    if request.user.is_authenticated:
        return redirect("core:home")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Auto-create profile
            Profile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, "Registration successful. Welcome!")
            return redirect("core:home")
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("core:home")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect("core:home")
    else:
        form = LoginForm(request)

    return render(request, "users/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("users:login")


@login_required
def profile_edit(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("users:dashboard")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "users/profile_edit.html", {"form": form})


@login_required
def dashboard(request):
    profile = request.user.profile
    my_applications = request.user.applications.select_related("job")
    my_jobs = request.user.jobs.all() if request.user.is_staff else []
    return render(
        request,
        "users/dashboard.html",
        {
            "profile": profile,
            "my_applications": my_applications,
            "my_jobs": my_jobs,
        },
    )
