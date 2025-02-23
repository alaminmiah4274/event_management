from django import forms
from tasks.forms import StyleFormMixin
from django.contrib.auth.models import User, Group, Permission
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.forms import AuthenticationForm


class CustomSignUpModelForm(StyleFormMixin, forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "password1",
            "confirm_password",
            "email",
        ]

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        errors = []

        if len(password1) < 8:
            errors.append("Password must be at least 8 characters long")

            if re.fullmatch(r"[A-Za-z0-9!@#$%^&*+=]", password1):
                errors.append(
                    "Password must be Uppercase, Lowercase, Number & special characters"
                )

        if errors:
            raise forms.ValidationError(errors)

        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("confirm_password")

        if password1 and confirm_password and password1 != confirm_password:
            raise forms.ValidationError("Password do not match")

        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get("email")
        email_exist = User.objects.filter(email=email).exists()

        if email_exist:
            raise ValidationError("The email is already in use")

        return email


class SignInForm(StyleFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CreateGroupModelForm(StyleFormMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label="Assign Group",
    )

    class Meta:
        model = Group
        fields = ["name", "permissions"]


class AssignRoleForm(StyleFormMixin, forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(), empty_label="Select A Role"
    )
