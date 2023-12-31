from django.urls import path

from . import views

urlpatterns = [
    path("cities/", views.CityList.as_view()),
    path("create/", views.CreateCafe.as_view()),
    path("<str:city>", views.CityCafes.as_view()),
    path("edit/<int:cafe_pk>", views.EditCafe.as_view()),
    path("detail/<int:cafe_pk>", views.CafeDetail.as_view()),
]
