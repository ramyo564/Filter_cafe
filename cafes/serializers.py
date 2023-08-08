from rest_framework import serializers
from .models import Cafe, BusinessDays, CafeBusinessHours, CafeOption, CafeReviews


class BusinessDaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessDays
        fields = "__all__"


class CafeOptionSerializer(serializers.ModelSerializer):
    option = serializers.CharField(source='cafe_option.name')

    class Meta:
        model = CafeOption
        fields = ('id', 'option', 'rating', 'sum_user', 'sum_rating')


class CafeBusinessHoursSerializer(serializers.ModelSerializer):
    business_days = BusinessDaysSerializer()

    class Meta:
        model = CafeBusinessHours
        fields = ('business_days', 'business_hours')


class CafeReviewsSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')

    class Meta:
        model = CafeReviews
        fields = "__all__"


class CafeSerializer(serializers.ModelSerializer):
    city_id = serializers.IntegerField(source='city.id', read_only=True)
    city = serializers.CharField(source='city.name', read_only=True)
    options = CafeOptionSerializer(many=True, source='cafe_option_cafe')
    business_hours = CafeBusinessHoursSerializer(
        many=True, source='cafe_business_hours_cafe'
    )
    cafe_reviews = CafeReviewsSerializer(many=True, source='cafe_reviews_cafe')

    class Meta:
        model = Cafe
        fields = "__all__"
