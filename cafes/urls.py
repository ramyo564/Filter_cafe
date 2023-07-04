from django.urls import path

from . import views

urlpatterns = [
    path("cities", views.CityList.as_view()),
    path("create", views.CreateCafe.as_view()),
    path("<str:city>", views.CityCafes.as_view()),
    path("edit/<int:cafe_pk>", views.EditCafe.as_view()),
    path("filter/", views.CafeFilter.as_view()),
    path("filter/<int:filter_pk>", views.CafeFilterDetail.as_view()),
]
