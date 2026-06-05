from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["push_notifications_enabled", "reminder_time"]
        widgets = {
            "reminder_time": forms.TimeInput(attrs={"type": "time"}),
        }
