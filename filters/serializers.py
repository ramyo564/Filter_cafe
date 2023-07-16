from rest_framework import serializers
from .models import City, Filter, Option


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = "__all__"


class FilterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Filter
        fields = "__all__"


class OptionSerializer(serializers.ModelSerializer):

    filter = FilterSerializer()

    class Meta:
        model = Option
        fields = "__all__"
