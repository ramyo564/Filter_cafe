import json
import pytest


pytestmark = pytest.mark.django_db


class TestUserEndpoints:

    endpoint = "/api/user/"

    def test_return_all_users(self, user_factory, api_client):
        # Arrange
        user_factory.create_batch(10)
        # Act
        response = api_client().get(self.endpoint)
        # Assert
        # print(f"response : {response}")
        # print(json.loads(response.content))
        assert response.status_code == 200

        assert len(json.loads(response.content)) == 10
