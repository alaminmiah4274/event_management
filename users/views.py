from django.shortcuts import render, redirect, HttpResponse
from users.forms import (
    CustomSignUpModelForm,
    SignInForm,
    CreateGroupModelForm,
    AssignRoleForm,
    EditProfileForm,
    CustomPasswordChangeForm,
    CustomPasswordResetForm,
    CustomPasswordResetConfirmForm,
)
from django.contrib.auth import login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
)
from django.db.models import Prefetch
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView, UpdateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView,
)
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import View


# Create your views here.

User = get_user_model()


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


# -------
class CreateGroupView(UserPassesTestMixin, View):
    template_name = "admin/create_group.html"
    login_url = "no-permission"

    def test_func(self):
        return is_admin(self.request.user)

    def get(self, request):
        form = CreateGroupModelForm()
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = CreateGroupModelForm(request.POST)

        if form.is_valid():
            group = form.save()
            messages.success(
                request, f"Group {group.name} has been created successfully"
            )
            return redirect("create-group")

        context = {"form": form}
        return render(request, self.template_name, context)


# ---------
class AssignRoleView(UserPassesTestMixin, FormView):
    template_name = "admin/assign_role.html"
    form_class = AssignRoleForm
    success_url = reverse_lazy("admin-dashboard")

    def test_func(self):
        return is_admin(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get("user_id")
        user = User.objects.get(id=user_id)
        context["user"] = user
        return context

    def form_valid(self, form):
        user_id = self.kwargs.get("user_id")
        user = User.objects.get(id=user_id)
        role = form.cleaned_data.get("role")

        user.groups.clear()
        user.groups.add(role)

        # success message
        messages.success(
            self.request,
            f"User {user.username} has been assigned to the {role.name} role",
        )

        return super().form_valid(form)


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


class ProfileView(TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context["username"] = user.username
        context["email"] = user.email
        context["name"] = user.get_full_name()
        context["phone"] = user.phone_number
        context["member_since"] = user.date_joined
        context["last_login"] = user.last_login
        context["profile_image"] = user.profile_image

        return context


class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = "accounts/update_profile.html"
    context_object_form = "form"
    success_url = reverse_lazy("profile")

    def get_object(self):
        return self.request.user

    def form_save(self, form):
        form.save()
        return super().form_save(form)


class ChangePassword(PasswordChangeView):
    template_name = "accounts/password_change.html"
    form_class = CustomPasswordChangeForm


class CustomPasswordResetView(PasswordResetView):
    template_name = "registration/reset_password.html"
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy("sign-in")
    html_email_template_name = "registration/reset_email.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["protocol"] = "https" if self.request.is_secure() else "http"
        context["domain"] = self.request.get_host()
        return context

    def form_valid(self, form):
        messages.success(self.request, "A reset email sent. Please check your email")
        return super().form_valid(form)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "registration/reset_password.html"
    form_class = CustomPasswordResetConfirmForm
    success_url = reverse_lazy("sign-in")

    def form_valid(self, form):
        messages.success(self.request, "Password has been reset successfully")
        return super().form_valid(form)


"""
wiz_khalifa: Lifa@2024-->Ifa@2024
kendra_sunderland: Land@2024
sabanna_bond: Anna@2024-->Banna@2024
andrew_tate: Rew@2024 | organizer
admin: admin@2024-->admin#2024
"""
