from django.urls import path
from . import views

app_name = "applications"

urlpatterns = [
    path('apply/<int:id>/', views.apply, name="apply_job"),
]
