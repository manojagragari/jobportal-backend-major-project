from django.shortcuts import render

# Create your views here.
def apply(request, id):
    return render(request, "applications/apply.html")
