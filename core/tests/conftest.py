import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient
from .factories import (
    CafeFactory,
    ReviewFactory,
    BusinessHoursFactory,
    CityFactory,
    FilterFactory,
    OptionFactory,
    UserFactory
)

register(CafeFactory)
register(ReviewFactory)
register(BusinessHoursFactory)
register(CityFactory)
register(FilterFactory)
register(OptionFactory)
register(UserFactory)


@pytest.fixture
def api_client():
    return APIClient
