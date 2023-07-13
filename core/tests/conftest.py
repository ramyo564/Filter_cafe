import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient
from .factories import (
    CafeFactory,
    ReviewFactory,
    CafeBusinessHoursFactory,
    CityFactory,
    FilterFactory,
    OptionFactory,
    UserFactory,
    BusinessDaysFactory,
    CafeOptionFactory,
)

register(BusinessDaysFactory)
register(CafeFactory)
register(ReviewFactory)
register(CafeBusinessHoursFactory)
register(CityFactory)
register(FilterFactory)
register(OptionFactory)
register(UserFactory)
register(CafeOptionFactory)


@pytest.fixture
def api_client():
    return APIClient
