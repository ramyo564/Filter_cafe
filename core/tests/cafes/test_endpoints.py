import json

import pytest

pytestmark = pytest.mark.django_db


class TestCafeEndpoints:
    endpoint = "/api/v1/"

    def test_return_all_city_cafes(self, cafe_factory, api_client):
        # Arrange
        cafe_factory.create_batch(10)
        # Act
        response = api_client().get(self.endpoint + "서울")
        # Assert
        assert response.status_code == 200
        print(f"response : {response}")
        print(json.loads(response.content))
        assert len(json.loads(response.content)) == 5
