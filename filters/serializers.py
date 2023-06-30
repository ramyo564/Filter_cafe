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


# class CafeCreateSerializer(ModelSerializer):
#     class Meta:
#         model = C
