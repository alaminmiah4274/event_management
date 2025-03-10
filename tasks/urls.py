from django.urls import path
from tasks.views import (
    organizer_dashboard,
    add_category,
    dashboard,
    participant_dashboard,
    participate,
    EventDetailView,
    EventCreateView,
    EventUpdateView,
    EventDeleteView,
)

urlpatterns = [
    path("organizer-dashboard/", organizer_dashboard, name="organizer-dashboard"),
    # path("create-event/", create_event, name="create-event"),
    path("create-event/", EventCreateView.as_view(), name="create-event"),
    # path("delete-event/<int:id>/", delete_event, name="delete-event"),
    path("delete-event/<int:id>/", EventDeleteView.as_view(), name="delete-event"),
    # path("update-event/<int:id>/", update_event, name="update-event"),
    path(
        "update-event/<int:event_id>/", EventUpdateView.as_view(), name="update-event"
    ),
    path("add-category/", add_category, name="add-category"),
    path("dashboard/", dashboard, name="dashboard"),
    path("participant-dashboard/", participant_dashboard, name="participant-dashboard"),
    path("participate/<int:event_id>/", participate, name="participate"),
    # path("event-detail/<int:event_id>/", event_detail_view, name="event-detail"),
    path(
        "event-detail/<int:event_id>/", EventDetailView.as_view(), name="event-detail"
    ),
]
