from rest_framework import serializers
from .models import User, UserRating
from cafes.serializers import CafeSerializer, CafeOptionSerializer


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class UserRatingSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    cafe = CafeSerializer()
    cafe_option = CafeOptionSerializer()

    class Meta:
        model = UserRating
        fields = "__all__"
