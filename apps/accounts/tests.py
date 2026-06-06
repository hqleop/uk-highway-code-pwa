from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(SECURE_SSL_REDIRECT=False)
class AuthenticationFlowTests(TestCase):
    def test_register_creates_profile_and_logs_user_in(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "learner",
                "email": "learner@example.com",
                "password1": "A9v!qL2m#R7tZp4",
                "password2": "A9v!qL2m#R7tZp4",
            },
            follow=True,
        )

        user = User.objects.get(username="learner")
        self.assertEqual(user.email, "learner@example.com")
        self.assertTrue(hasattr(user, "userprofile"))
        self.assertRedirects(response, reverse("accounts:profile"))

    def test_login_accepts_email_or_username(self):
        User.objects.create_user(
            username="driver",
            email="driver@example.com",
            password="A9v!qL2m#R7tZp4",
        )

        email_response = self.client.post(
            reverse("accounts:login"),
            {"username": "driver@example.com", "password": "A9v!qL2m#R7tZp4"},
        )
        self.assertRedirects(email_response, reverse("accounts:profile"))

        self.client.logout()

        username_response = self.client.post(
            reverse("accounts:login"),
            {"username": "driver", "password": "A9v!qL2m#R7tZp4"},
        )
        self.assertRedirects(username_response, reverse("accounts:profile"))
