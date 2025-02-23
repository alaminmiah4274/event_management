from django.shortcuts import render, redirect, HttpResponse
from users.forms import (
    CustomSignUpModelForm,
    SignInForm,
    CreateGroupModelForm,
    AssignRoleForm,
)
from django.contrib.auth import login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
)
from django.db.models import Prefetch


# Create your views here.


# for user test
def is_admin(user):
    return user.groups.filter(name="Admin").exists()


def sign_up(request):
    form = CustomSignUpModelForm()

    if request.method == "POST":
        form = CustomSignUpModelForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get("password1"))
            user.is_active = False
            user.save()

            messages.success(
                request, "A confirmation mail has sent. Please check your email"
            )
            return redirect("sign-in")

    context = {"form": form}

    return render(request, "registration/sign_up.html", context)


def sign_in(request):
    form = SignInForm()

    if request.method == "POST":
        form = SignInForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")

    context = {"form": form}

    return render(request, "registration/sign_in.html", context)


@login_required
def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect("sign-in")

    return render(request, "home.html")


def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect("sign-in")
        else:
            return HttpResponse("Invalid id or token")
    except User.DoesNotExist:
        return HttpResponse("User Not Found!")


@user_passes_test(is_admin, login_url="no-permission")
def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch("groups", queryset=Group.objects.all(), to_attr="all_groups")
    ).all()

    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = "No Group Assigned"

    context = {"users": users}

    return render(request, "admin/dashboard.html", context)


@user_passes_test(is_admin, login_url="no-permission")
def create_group(request):
    form = CreateGroupModelForm()

    if request.method == "POST":
        form = CreateGroupModelForm(request.POST)

        if form.is_valid():
            group = form.save()

            messages.success(
                request, f"Group {group.name} has been created successfully"
            )
            return redirect("create-group")

    context = {"form": form}

    return render(request, "admin/create_group.html", context)


@user_passes_test(is_admin, login_url="no-permission")
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()

    if request.method == "POST":
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get("role")
            user.groups.clear()
            user.groups.add(role)

            messages.success(
                request,
                f"User {user.username} has been assigned to the {role.name} role",
            )
            return redirect("admin-dashboard")

    context = {"form": form}

    return render(request, "admin/assign_role.html", context)


@user_passes_test(is_admin, login_url="no-permission")
def group_list(request):
    groups = Group.objects.all()

    context = {"groups": groups}

    return render(request, "admin/group_list.html", context)


@user_passes_test(is_admin, login_url="no-permission")
def group_details(request, group_id):
    detail = Group.objects.prefetch_related("permissions").get(id=group_id)

    context = {"detail": detail}

    return render(request, "admin/group_details.html", context)


@user_passes_test(is_admin, login_url="no-permission")
def delete_participant(request, participant_id):
    if request.method == "POST":
        participant = User.objects.get(id=participant_id)
        participant.delete()

        messages.success(request, "participant deleted successfully")
        return redirect("admin-dashboard")
    else:
        messages.error(request, "something went wrong")
        return redirect("delete-participant", participant_id)


@user_passes_test(is_admin, login_url="no-permission")
def delete_group(request, group_id):
    if request.method == "POST":
        group = Group.objects.get(id=group_id)
        group.delete()

        messages.success(request, "group deleted successfully")
        return redirect("group-list")
    else:
        messages.error(request, "something went wrong")
        return redirect("delete-group", group_id)


"""
wiz_khalifa: Zwi@2024
admin: admin@5078
kendra_sunderland: Land@2024
sabanna_bond: Anna@2024
andrew_tate: Rew@2024
dance_party: Ance@2024
admin: admin@2024
"""
