from rest_framework import serializers
from .models import Cafe, Review, BusinessDays, CafeBusinessHours, CafeOption
from users.serializers import UserSerializer


class BusinessDaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessDays
        fields = "__all__"


class CafeOptionSerializer(serializers.ModelSerializer):
    option = serializers.CharField()

    class Meta:
        model = CafeOption
        fields = ('id', 'option', 'point')


class CafeBusinessHoursSerializer(serializers.ModelSerializer):
    business_days = BusinessDaysSerializer()

    class Meta:
        model = CafeBusinessHours
        fields = ('business_days', 'business_hours')


class CafeSerializer(serializers.ModelSerializer):
    city_id = serializers.IntegerField(source='city.id', read_only=True)
    city = serializers.CharField(source='city.name', read_only=True)
    options = CafeOptionSerializer(many=True, source='cafe_option_cafe')
    business_hours = CafeBusinessHoursSerializer(
        many=True, source='cafe_business_hours_cafe'
    )

    class Meta:
        model = Cafe
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    cafe = CafeSerializer()

    class Meta:
        model = Review
        fields = "__all__"
