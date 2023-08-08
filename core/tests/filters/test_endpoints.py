import json
import pytest


pytestmark = pytest.mark.django_db


class TestCityEndpoints:

    endpoint = "/api/city/"

    def test_return_all_cites(self, city_factory, api_client):
        # Arrange
        city_factory.create_batch(10)
        # Act
        response = api_client().get(self.endpoint)
        # Assert
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 10


class TestFilterEndpoints:

    endpoint = "/api/filter/"

    def test_return_all_filters(self, filter_factory, api_client):
        # Arrange
        filter_factory.create_batch(10)
        # Act
        response = api_client().get(self.endpoint)
        # Assert
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 10


class TestOptionEndpoints:

    endpoint = "/api/option/"

    def test_return_all_options(self, option_factory, api_client):
        # Arrange
        option_factory.create_batch(10)
        # Act
        response = api_client().get(self.endpoint)
        # Assert
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 10
