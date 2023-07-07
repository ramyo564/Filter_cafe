import json
import pytest


pytestmark = pytest.mark.django_db


class TestCafeEndpoints:

    endpoint = "/api/cafe/"

    def test_return_all_cafes(self, cafe_factory, api_client):
        # Arrange
        cafe_factory.create_batch(10)
        # Act
        response = api_client().get(self.endpoint)
        # Assert
        assert response.status_code == 200
        print(f"response : {response}")
        print(json.loads(response.content))
        assert len(json.loads(response.content)) == 10


class TestReviewEndpoints:

    endpoint = "/api/review/"

    def test_return_all_reviews(self, review_factory, api_client):
        # Arrange
        review_factory.create_batch(10)
        # Act
        response = api_client().get(self.endpoint)
        # Assert
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 10


class TestBusinessHoursEndpoints:

    endpoint = "/api/businesshours/"

    def test_return_all_businesshours(self, business_hours_factory, api_client):
        # Arrange
        business_hours_factory.create_batch(10)
        # Act
        response = api_client().get(self.endpoint)
        # Assert
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 10
