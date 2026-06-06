from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import UserProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class EmailOrUsernameAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username or email")

    def clean(self):
        identifier = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if identifier is not None and password:
            username = identifier
            if "@" in identifier:
                user = User.objects.filter(email__iexact=identifier).first()
                if user is not None:
                    username = user.get_username()

            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise ValidationError(
                    self.error_messages["invalid_login"],
                    code="invalid_login",
                    params={"username": self.username_field.verbose_name},
                )
            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["push_notifications_enabled", "reminder_time"]
        widgets = {
            "reminder_time": forms.TimeInput(attrs={"type": "time"}),
        }
