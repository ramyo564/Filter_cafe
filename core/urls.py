"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from cafes import views as cafe_views
from users import views as user_views
from filters import views as filter_views


router = DefaultRouter()
router.register(r"cafe", cafe_views.CafeViewSet)
router.register(r"review", cafe_views.ReviewViewSet)
router.register(r"city", filter_views.CityViewSet)
router.register(r"filter", filter_views.FilterViewSet)
router.register(r"option", filter_views.OptionViewSet)
router.register(r"user", user_views.UserViewSet)

# test
urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/docs/", SpectacularSwaggerView.as_view(url_name="schema")),

]
