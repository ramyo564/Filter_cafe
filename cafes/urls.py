from django.urls import path

from . import views

urlpatterns = [
    path("cities", views.CityList.as_view()),
    path("<str:city>", views.CityCafes.as_view()),
]
