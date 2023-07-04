from django.urls import path

from . import views

urlpatterns = [
    path("", views.CafeFilter.as_view()),
    path("score/", views.CafeFilterScore.as_view()),
    path("<int:filter_pk>", views.CafeFilterDetail.as_view()),
    path("score/<int:filter_score_pk>", views.CafeFilterScoreDetail.as_view()),
]
