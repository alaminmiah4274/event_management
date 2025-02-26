from django.urls import path
from tasks.views import (
    organizer_dashboard,
    create_event,
    delete_event,
    update_event,
    add_category,
    dashboard,
    participant_dashboard,
    participate,
)

urlpatterns = [
    path("organizer-dashboard/", organizer_dashboard, name="organizer-dashboard"),
    path("create-event/", create_event, name="create-event"),
    path("delete-event/<int:id>/", delete_event, name="delete-event"),
    path("update-event/<int:id>/", update_event, name="update-event"),
    path("add-category/", add_category, name="add-category"),
    path("dashboard/", dashboard, name="dashboard"),
    path("participant-dashboard/", participant_dashboard, name="participant-dashboard"),
    path("participate/<int:event_id>/", participate, name="participate"),
]
