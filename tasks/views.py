from django.shortcuts import render, redirect
from tasks.models import Event
from django.db.models import Q, Count
from datetime import date
from tasks.forms import EventModelForm, CategoryModelForm
from django.contrib import messages
from django.contrib.auth.decorators import (
    permission_required,
    login_required,
)
from users.views import is_admin
from django.contrib.auth import get_user_model
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.views import View


User = get_user_model()


# Create your views here.
def is_organizer(user):
    return user.groups.filter(name="Organizer").exists()


def is_participant(user):
    return user.groups.filter(name="Participant").exists()


def load_counts():
    counts = Event.objects.aggregate(
        total_events=Count("id", distinct=True),
        total_participants=Count("participant", distinct=True),
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


# ------
class EventCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = "form/event_form.html"
    success_url = reverse_lazy("create-event")
    permission_required = "tasks.add_event"
    login_url = "no-permission"

    def get(self, request, *args, **kwargs):
        event_form = EventModelForm()
        context = {"event_form": event_form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        event_form = EventModelForm(request.POST, request.FILES)

        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event Created Successfully")
        else:
            messages.error(request, "The event date cannot be in the past.")
            # Instead of redirecting on error, we'll render the form with errors
            context = {"event_form": event_form}
            return render(request, self.template_name, context)


# ----------
class EventUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = "form/event_form.html"
    permission_required = "tasks.change_event"
    login_url = "no-permission"
    pk_url_kwarg = "event_id"

    def get(self, request, event_id):
        event = Event.objects.get(id=event_id)
        event_form = EventModelForm(instance=event)
        context = {"event_form": event_form}
        return render(request, self.template_name, context)

    def post(self, request, event_id):
        event = Event.objects.get(id=event_id)
        event_form = EventModelForm(request.POST, request.FILES, instance=event)

        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event Updated Successfully")
            return redirect("update-event", event_id=event_id)

        context = {"event_form": event_form}
        return render(request, self.template_name, context)


# -------
class EventDeleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "tasks.delete_event"
    login_url = "no-permission"

    def post(self, request, id):
        try:
            event = Event.objects.get(id=id)
            event.delete()
            messages.success(request, "Event Deleted Successfully")
            return redirect("organizer-dashboard")
        except Event.DoesNotExist:
            messages.error(request, "Event not found")
            return redirect("organizer-dashboard")

    def get(self, request, id):
        messages.error(request, "Something Went Wrong")
        return redirect("delete-event", id=id)


@login_required
@permission_required("tasks.view_event", login_url="no-permission")
def organizer_dashboard(request):
    type = request.GET.get("type", "all")

    base_query = Event.objects.select_related("category").prefetch_related(
        "participant"
    )

    if type == "upcoming":
        events = base_query.filter(date__gt=date.today())

    elif type == "previous":
        events = base_query.filter(date__lt=date.today())

    elif type == "all":
        events = base_query.all()

    context = {"events": events, "counts": load_counts()}

    return render(request, "dashboard/organizer_dashboard.html", context)


@login_required
def dashboard(request):
    if is_organizer(request.user):
        return redirect("organizer-dashboard")
    elif is_admin(request.user):
        return redirect("admin-dashboard")
    elif is_participant(request.user):
        return redirect("participant-dashboard")

    return redirect("no-permission")


@login_required
def participant_dashboard(request):
    user = request.user
    events = user.event.all().select_related("category")

    context = {"events": events}

    return render(request, "dashboard/participant_dashboard.html", context)


@login_required
def participate(request, event_id):
    if request.method == "POST":
        event = Event.objects.get(id=event_id)
        if request.user.is_authenticated:
            user = request.user
            if event in user.event.all():
                messages.warning(
                    request, "You have already participated in this event."
                )
            else:
                user.event.add(event)
                messages.success(
                    request, "You have successfully participated in the event."
                )
                return redirect("home")
    else:
        messages.error(request, "You must be logged in to participate.")
        return redirect("home")


class EventDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Event
    template_name = "event_details.html"
    context_object_name = "event"
    pk_url_kwarg = "event_id"
    login_url = "no-permission"
    permission_required = "tasks.view_event"
