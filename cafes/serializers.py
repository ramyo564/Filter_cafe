from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from filters.models import BallotBox, Filter, FilterScore
from users.models import User

from .models import BusinessHours, Cafe, Review


class BusinessHoursSerializer(ModelSerializer):
    class Meta:
        model = BusinessHours
        fields = "__all__"


class CafesSerializer(ModelSerializer):
    business_hours = BusinessHoursSerializer(
        read_only=True,
    )

    class Meta:
        model = Cafe
        fields = (
            "pk",
            "name",
            "city",
            "address",
            "business_hours",
        )


class CafeCreateSerializer(ModelSerializer):
    class Meta:
        model = Cafe
        fields = (
            "name",
            "address",
        )
