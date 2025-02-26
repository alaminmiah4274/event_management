from django.shortcuts import render
from tasks.models import Event
from datetime import date

# Create your views here.


def home(request):
    upcoming_events = Event.objects.select_related("category").filter(
        date__gt=date.today()
    )

    today_events = Event.objects.select_related("category").filter(date=date.today())

    context = {"today_events": today_events, "upcoming_events": upcoming_events}

    return render(request, "home/home.html", context)


def no_permission(request):
    return render(request, "no_permission.html")
