from django.urls import path

from . import views


app_name = "rules"

urlpatterns = [
    path("", views.section_list, name="section_list"),
    path("search/", views.search, name="search"),
    path("<slug:section_slug>/", views.section_detail, name="section_detail"),
    path("<slug:section_slug>/<str:rule_number>/", views.rule_detail, name="rule_detail"),
]
