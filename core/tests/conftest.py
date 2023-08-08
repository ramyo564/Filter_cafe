import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient
from .factories import (
    CafeFactory,
    UserRatingFactory,
    CafeBusinessHoursFactory,
    CafeReviewsFactory,
    CityFactory,
    FilterFactory,
    OptionFactory,
    UserFactory,
    BusinessDaysFactory,
    CafeOptionFactory,
)

register(BusinessDaysFactory)
register(CafeFactory)
register(UserRatingFactory)
register(CafeBusinessHoursFactory)
register(CityFactory)
register(FilterFactory)
register(OptionFactory)
register(UserFactory)
register(CafeOptionFactory)
register(CafeReviewsFactory)


@pytest.fixture
def api_client():
    return APIClient
