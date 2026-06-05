from django.urls import path

from . import views


app_name = "daily"

urlpatterns = [
    path("", views.today, name="today"),
    path("answer/", views.answer, name="answer"),
]
