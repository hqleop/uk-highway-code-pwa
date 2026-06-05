from django.urls import path

from . import views


app_name = "quiz"

urlpatterns = [
    path("", views.quiz_home, name="home"),
    path("start/", views.start, name="start"),
    path("session/<uuid:session_id>/", views.session, name="session"),
    path("answer/", views.answer, name="answer"),
    path("results/<uuid:session_id>/", views.results, name="results"),
]
