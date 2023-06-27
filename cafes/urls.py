from django.urls import path

from . import views

urlpatterns = [
    path("<str:city>", views.CityCafes.as_view()),
    path("cities", views.CityList.as_view()),
]
