import pytest

pytestmark = pytest.mark.django_db


class TestCityModel:
    def test_str_method(self, city_factory):

        x = city_factory(name="test_city")

        assert x.__str__() == "test_city"


class TestFilterModel:
    def test_str_method(self, filter_factory):

        x = filter_factory(name="test_filter")

        assert x.__str__() == "test_filter"


class TestOptionModel:
    def test_str_method(self, option_factory):

        x = option_factory(name="test_option")

        assert x.__str__() == "test_option"
