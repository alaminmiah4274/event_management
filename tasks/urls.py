from django.urls import path
from tasks.views import admin_dashboard, create_event, delete_event, update_event, add_participant, add_category, today_events

urlpatterns = [
	path("admin-dashboard/", admin_dashboard, name = "admin-dashboard"),
	path("create-event/", create_event, name = "create-event"),
	path("delete-event/<int:id>/", delete_event, name = "delete-event"),
	path("update-event/<int:id>/", update_event, name = "update-event"),
	path("add-category/", add_category, name = "add-category"),
	path("add-participant/", add_participant, name = "add-participant"),
	path("today-events/", today_events, name = "today-events")
]