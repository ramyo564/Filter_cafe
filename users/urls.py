from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.Signup.as_view()),
    path("login/", views.LogIn.as_view()),
    path("logout/", views.LogOut.as_view()),
    path("info/", views.UserInformation.as_view()),
    path("kakao/", views.KakaoLogIn.as_view()),
]
