from django.urls import path
from users.views import (
    sign_up,
    sign_in,
    sign_out,
    activate_user,
    admin_dashboard,
    create_group,
    assign_role,
    group_list,
    group_details,
    delete_participant,
    delete_group,
)

urlpatterns = [
    path("sign-up/", sign_up, name="sign-up"),
    path("sign-in/", sign_in, name="sign-in"),
    path("sign-out/", sign_out, name="sign-out"),
    path("activate/<int:user_id>/<str:token>/", activate_user),
    path("admin/dashboard/", admin_dashboard, name="admin-dashboard"),
    path("admin/create-group", create_group, name="create-group"),
    path("admin/assign-role/<int:user_id>/", assign_role, name="assign-role"),
    path("admin/group-list/", group_list, name="group-list"),
    path("admin/group-details/<int:group_id>/", group_details, name="group-details"),
    path(
        "admin/delete-participant/<int:participant_id>/",
        delete_participant,
        name="delete-participant",
    ),
    path("admin/delete-group/<int:group_id>/", delete_group, name="delete-group"),
]
