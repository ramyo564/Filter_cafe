from rest_framework.serializers import ModelSerializer

from cafes.models import Cafe, Review
from filters.models import BallotBox, Filter, FilterScore
from users.models import User


class BallotBoxSerializer(ModelSerializer):
    class Meta:
        model = BallotBox
        fields = (
            "pk",
            "cafe",
            "filter",
            "score",
        )


class FilterSerializer(ModelSerializer):
    class Meta:
        model = Filter
        fields = (
            "pk",
            "name",
        )


class FilterScoreSerializer(ModelSerializer):
    class Meta:
        model = FilterScore
        fields = (
            "pk",
            "score",
        )
