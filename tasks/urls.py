from django.urls import path
from tasks.views import admin_dashboard, create_event, delete_event, update_event

urlpatterns = [
	path("admin-dashboard/", admin_dashboard, name = "admin-dashboard"),
	path("create-event/", create_event, name = "create-event"),
	path("delete-event/<int:id>/", delete_event, name = "delete-event"),
	path("update-event/<int:id>/", update_event, name = "update-event"),
]