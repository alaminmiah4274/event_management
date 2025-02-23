from django.shortcuts import render, redirect
from tasks.models import Event
from django.db.models import Q, Count
from datetime import date
from tasks.forms import EventModelForm, CategoryModelForm
from django.contrib import messages
from django.contrib.auth.decorators import (
    permission_required,
    login_required,
    user_passes_test,
)
from users.views import is_admin


# Create your views here.
def is_organizer(user):
    return user.groups.filter(name="Organizer").exists()


def is_participant(user):
    return user.groups.filter(name="Participant").exists()


def load_counts():
    counts = Event.objects.aggregate(
        total_events=Count("id", distinct=True),
        total_participants=Count("user", distinct=True),
        upcoming=Count("id", distinct=True, filter=Q(date__gt=date.today())),
        previous=Count("id", distinct=True, filter=Q(date__lt=date.today())),
    )

    return counts


@login_required
@permission_required("tasks.add_category", login_url="no-permission")
def add_category(request):
    category_form = CategoryModelForm()

    if request.method == "POST":
        category_form = CategoryModelForm(request.POST)

        if category_form.is_valid():
            category_form.save()

            messages.success(request, "Category Created Successfully")
            return redirect("add-category")

    context = {"category_form": category_form}

    return render(request, "form/category_form.html", context)


@login_required
@permission_required("tasks.add_event", login_url="no-permission")
def create_event(request):
    event_form = EventModelForm()

    if request.method == "POST":
        event_form = EventModelForm(request.POST, request.FILES)

        if event_form.is_valid():
            event_form.save()

            messages.success(request, "Event Created Successfully")
            return redirect("create-event")
        else:
            messages.error(request, "The event date cannot be in the past.")
            return redirect("create-event")

    context = {"event_form": event_form}

    return render(request, "form/event_form.html", context)


@login_required
@permission_required("tasks.change_event", login_url="no-permission")
def update_event(request, id):
    event = Event.objects.get(id=id)
    event_form = EventModelForm(instance=event)

    if request.method == "POST":
        event_form = EventModelForm(request.POST, instance=event)

        if event_form.is_valid():
            event_form.save()

            messages.success(request, "Event Updated Successfully")
            return redirect("update-event", id)

    context = {"event_form": event_form}

    return render(request, "form/event_form.html", context)


@login_required
@permission_required("tasks.delete_event", login_url="no-permission")
def delete_event(request, id):
    if request.method == "POST":
        event = Event.objects.get(id=id)
        event.delete()

        messages.success(request, "Task Deleted Successfully")
        return redirect("organizer-dashboard")
    else:
        messages.error(request, "Something Went Wrong")
        return redirect("delete-event", id)


@login_required
@permission_required("tasks.view_event", login_url="no-permission")
def organizer_dashboard(request):
    print("from is_admin:", request.user.get_all_permissions())

    type = request.GET.get("type", "all")

    base_query = Event.objects.select_related("category").prefetch_related("user")
    todays = base_query.filter(date=date.today())

    if type == "upcoming":
        events = base_query.filter(date__gt=date.today())

    elif type == "previous":
        events = base_query.filter(date__lt=date.today())

    elif type == "all":
        events = base_query.all()

    context = {"events": events, "counts": load_counts(), "todays": todays}

    return render(request, "dashboard/organizer_dashboard.html", context)


# def today_events(request):
#     todays = (
#         Event.objects.select_related("category")
#         .prefetch_related("participant")
#         .filter(date=date.today())
#     )

#     context = {"todays": todays}

#     return render(request, "today_events/today_events.html", context)


@login_required
def dashboard(request):
    if is_organizer(request.user):
        return redirect("organizer-dashboard")
    elif is_admin(request.user):
        return redirect("admin-dashboard")
    elif is_participant(request.user):
        return redirect("participant-dashboard")

    return redirect("no-permission")


def participant_dashboard(request):
    context = {}

    return render(request, "dashboard/participant_dashboard.html", context)
