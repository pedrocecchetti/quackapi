from django.contrib.auth.admin import UserAdmin

from django.contrib import admin

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User


class UserCreateForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """

    password1 = forms.CharField(label="Senha", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmação", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas são diferentes")

        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        return user


class UserUpdateForm(forms.ModelForm):
    """
    A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    password = ReadOnlyPasswordHashField(label="Senha:")

    class Meta:
        model = User
        fields = ("email", "password", "is_active", "is_superuser")

    def clean_password(self):
        """
        Regardless of what the user provides, return the initial value.
        This is done here, rather than on the field, because the
        field does not have access to the initial value
        """
        return self.initial["password"]


class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    add_form = UserCreateForm
    form = UserUpdateForm
    empty_value_display = "----"

    readonly_fields = ["created_at", "updated_at"]

    # The fields to be used in displaying the User model.
    list_display = (
        "first_name",
        "last_name",
        "email",
        "last_login",
        "is_active",
        "is_superuser",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "first_name",
        "last_name",
        "email",
        "last_login",
        "is_active",
        "is_superuser",
        "created_at",
        "updated_at",
    )

    # The fields to be used in updates on User model.
    fieldsets = (
        (
            "Informações básicas",
            {
                "classes": ("grp-collapse grp-open",),
                "fields": (("first_name", "last_name"), "email", "password"),
            },
        ),
        (
            "Permissões",
            {"classes": ("grp-collapse grp-open",), "fields": ("is_superuser",)},
        ),
        ("Status", {"classes": ("grp-collapse grp-open",), "fields": ("is_active",)}),
    )

    # The fields to be used in inserts on User model.
    add_fieldsets = (
        (
            "Login",
            {
                "classes": ("grp-collapse grp-open", "wide"),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    # Search and ordering
    search_fields = (
        "first_name",
        "last_name",
        "email",
        "last_login",
        "is_active",
        "is_superuser",
        "created_at",
        "updated_at",
    )

    ordering = ("first_name", "created_at")
    filter_horizontal = ()


admin.site.register(User, CustomUserAdmin )
