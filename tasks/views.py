from django.shortcuts import render, redirect
from tasks.models import Event, Participant, Category
from django.db.models import Q, Count, Sum
from datetime import date
from tasks.forms import EventModelForm, ParticipantModelForm, CategoryModelForm
from django.contrib import messages

# Create your views here.

def load_counts():
	counts = Event.objects.aggregate(
		total_events = Count("id", distinct = True),
		total_participants = Count("participant", distinct = True),
		upcoming = Count("id", distinct = True, filter = Q(date__gt = date.today())),
		previous = Count("id", distinct = True, filter = Q(date__lt = date.today()))
	)

	return counts



def add_category(request):
	category_form = CategoryModelForm()

	if request.method == "POST":
		category_form = CategoryModelForm(request.POST)

		if category_form.is_valid():
			category = category_form.save()


			messages.success(request, "Category Created Successfully")
			return redirect("add-category")


	context = {
		"category_form": category_form
	}

	return render(request, "form/category_form.html", context)



def create_event(request):
	event_form = EventModelForm()

	if request.method == "POST":
		event_form = EventModelForm(request.POST)

		if event_form.is_valid():
			event_form.save()

			messages.success(request, "Event Created Successfully")
			return redirect("create-event")
		else:
			messages.error(request, "The event date cannot be in the past.")
			return redirect("create-event")


	context = {
		"event_form": event_form
	}

	return render(request, "form/event_form.html", context)


def add_participant(request):
	participant_form = ParticipantModelForm()

	if request.method == "POST":
		participant_form = ParticipantModelForm(request.POST)

		if participant_form.is_valid():
			participant = participant_form.save()
			print("object:", participant)

			messages.success(request, "Participant Created Successfully")
			return redirect("add-participant")
		else:
			print("error:", participant_form.errors)


	context = {
		"participant_form": participant_form
	}

	return render(request, "form/participant_form.html", context)



def update_event(request, id):
	event = Event.objects.get(id = id)
	event_form = EventModelForm(instance = event)

	if request.method == "POST":
		event_form = EventModelForm(request.POST, instance = event)

		if event_form.is_valid():
			event_form.save()

			messages.success(request, "Event Updated Successfully")
			return redirect("update-event", id)


	context = {
		"event_form": event_form
	}

	return render(request, "form/event_form.html", context)



def delete_event(request, id):
	if request.method == "POST":
		event = Event.objects.get(id = id)
		event.delete()

		messages.success(request, "Task Deleted Successfully")
		return redirect("admin-dashboard")
	else:
		messages.error(request, "Something Went Wrong")
		return redirect("delete-event", id)



def admin_dashboard(request):
	type = request.GET.get("type", "all")
	
	base_query = Event.objects.select_related("category").prefetch_related("participant")
	todays = base_query.filter(date = date.today())

	if type == "upcoming":
		events = base_query.filter(date__gt = date.today())
		
	elif type == "previous":
		events = base_query.filter(date__lt = date.today())
		
	elif type == "all":
		events = base_query.all()
		


	context = {
		"events": events,
		"counts": load_counts(),
		"todays": todays
	}

	return render(request, "dashboard/admin_dashboard.html", context)


def today_events(request):
	todays = Event.objects.select_related("category").prefetch_related("participant").filter(date = date.today())

	context = {
		"todays": todays
	}

	return render(request, "today_events/today_events.html", context)