from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from accounts.models import UserProfile


class UserProfileForm(forms.ModelForm):

    first_name = forms.CharField(
        label="Vorname",
        max_length=150,
        required=True,
    )

    last_name = forms.CharField(
        label="Nachname",
        max_length=150,
        required=True,
    )

    email = forms.EmailField(
        label="Firmen-E-Mail",
        required=True,
    )

    password = forms.CharField(
        label="Passwort",
        required=False,
        widget=forms.PasswordInput(),
    )

    password_confirm = forms.CharField(
        label="Passwort wiederholen",
        required=False,
        widget=forms.PasswordInput(),
    )

    class Meta:

        model = UserProfile

        fields = (
            "first_name",
            "last_name",
            "email",
            "entry_date",
            "category",
            "etcs_level1",
            "etcs_level2",
            "role",
            "active",
        )

        labels = {
            "entry_date": "Eintrittsdatum",
            "category": "Kategorie",
            "etcs_level1": "ETCS Level 1",
            "etcs_level2": "ETCS Level 2",
            "role": "Rolle",
            "active": "Aktiv",
        }

        widgets = {
            "role": forms.RadioSelect,
            "etcs_level1": forms.CheckboxInput,
            "etcs_level2": forms.CheckboxInput,
            "active": forms.CheckboxInput,
        }

    def __init__(self, *args, **kwargs):

        super().__init__(
            *args,
            **kwargs
        )

        if self.instance and self.instance.pk:

            user = self.instance.user

            self.fields["first_name"].initial = (
                user.first_name
            )

            self.fields["last_name"].initial = (
                user.last_name
            )

            self.fields["email"].initial = (
                user.email
            )

            self.fields["password"].help_text = (
                "Leer lassen, wenn das bisherige "
                "Passwort beibehalten werden soll."
            )

        else:

            self.fields["password"].required = True
            self.fields["password_confirm"].required = True

    def clean_email(self):

        email = (
            self.cleaned_data["email"]
            .strip()
            .lower()
        )

        users = User.objects.filter(
            username=email
        )

        if self.instance and self.instance.pk:

            users = users.exclude(
                pk=self.instance.user.pk
            )

        if users.exists():

            raise forms.ValidationError(
                "Diese Firmen-E-Mail-Adresse "
                "wird bereits verwendet."
            )

        return email

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get(
            "password"
        )

        password_confirm = cleaned_data.get(
            "password_confirm"
        )

        if password or password_confirm:

            if password != password_confirm:

                raise forms.ValidationError(
                    "Die Passwörter stimmen nicht überein."
                )

            validate_password(
                password,
                self.instance.user
                if self.instance and self.instance.pk
                else None
            )

        return cleaned_data

    def save(self, commit=True):

        profile = super().save(
            commit=False
        )

        email = (
            self.cleaned_data["email"]
        )

        if profile.pk:

            user = profile.user

            user.first_name = (
                self.cleaned_data["first_name"]
            )

            user.last_name = (
                self.cleaned_data["last_name"]
            )

            user.email = email
            user.username = email

        else:

            user = User.objects.create_user(
                username=email,
                email=email,
                first_name=self.cleaned_data[
                    "first_name"
                ],
                last_name=self.cleaned_data[
                    "last_name"
                ],
                password=self.cleaned_data[
                    "password"
                ],
            )

            profile.user = user

        password = (
            self.cleaned_data.get("password")
        )

        if password:

            user.set_password(
                password
            )

        # Profilstatus und Loginstatus
        # immer synchron halten.

        user.is_active = bool(
            profile.active
        )

        # Rollenrechte

        if profile.role == "admin":

            user.is_staff = True
            user.is_superuser = False

        else:

            user.is_staff = False
            user.is_superuser = False

        if commit:

            user.save()

            profile.save()

        return profile