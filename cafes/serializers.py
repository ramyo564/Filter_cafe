from rest_framework import serializers
from .models import Cafe, Review, BusinessHours
from filters.serializers import OptionSerializer
from users.serializers import UserSerializer


class CafeSerializer(serializers.ModelSerializer):

    options = serializers.SerializerMethodField()
    business_hours = serializers.SerializerMethodField()

    class Meta:
        model = Cafe
        fields = "__all__"

    def get_business_hours(self, obj):
        business_hours = obj.business_hours
        return {
            "mon": business_hours.mon,
            "tue": business_hours.tue,
            "wed": business_hours.wed,
            "thu": business_hours.thu,
            "fri": business_hours.fri,
            "sat": business_hours.sat,
            "sun": business_hours.sun,
        }

    def get_options(self, obj):
        options = obj.options.all()
        return OptionSerializer(options, many=True).data


class ReviewSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    cafe = CafeSerializer()

    class Meta:
        model = Review
        fields = "__all__"


class BusinessHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessHours
        fields = "__all__"
