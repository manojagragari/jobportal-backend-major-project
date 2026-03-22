from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path('', views.home, name="home"),
    path('jobs/', views.jobs, name="jobs"),
    path('jobs/<int:pk>/', views.job_detail, name="job_detail"),
    path('jobs/create/', views.create_job, name="job_create"),
]
