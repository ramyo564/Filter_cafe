from rest_framework import serializers
from .models import Cafe, Review, BusinessDays, CafeBusinessHours, CafeOption
from filters.serializers import OptionSerializer
from users.serializers import UserSerializer


class BusinessDaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessDays
        fields = "__all__"


class CafeSerializer(serializers.ModelSerializer):
    city_id = serializers.IntegerField(source='city.id', read_only=True)
    city = serializers.CharField(source='city.name', read_only=True)

    class Meta:
        model = Cafe
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    cafe = CafeSerializer()

    class Meta:
        model = Review
        fields = "__all__"


class CafeBusinessHoursSerializer(serializers.ModelSerializer):

    cafes = CafeSerializer()
    BusinessDays = BusinessDaysSerializer()

    class Meta:
        model = CafeBusinessHours
        fields = "__all__"


class CafeOptionSerializer(serializers.ModelSerializer):

    cafe = CafeSerializer()
    option = OptionSerializer()

    class Meta:
        model = CafeOption
        fields = "__all__"
