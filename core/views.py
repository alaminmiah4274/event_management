from django.shortcuts import render
from tasks.models import Event
from datetime import date

# Create your views here.


def home(request):
    todays = (
        Event.objects.select_related("category")
        .prefetch_related("participant")
        .filter(date=date.today())
    )

    context = {"todays": todays}

    return render(request, "home.html", context)


def no_permission(request):
    return render(request, "no_permission.html")
