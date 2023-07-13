import json
import pytest


pytestmark = pytest.mark.django_db


class TestCafeEndpoints:

    endpoint = "/api/cafe/"

    def test_return_all_cafes(self, cafe_factory, api_client):
        # Arrange
        cafe_factory.create_batch(10)
        # Act
        response = api_client().get(path=self.endpoint)
        # Assert
        assert response.status_code == 200
        # print(f"response : {response}")
        # print(response.json())
        assert len(response.json()) == 10

    def test_return_all_cafes_by_city(self, cafe_factory, city_factory, api_client):
        city_slug = city_factory(slug="서울")
        cafe_factory(city=city_slug)
        response = api_client().get(f"{self.endpoint}{city_slug.slug}/")
        print(response.json())
        # Assert
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_return_all_cafes_by_city_option(
        self,
        cafe_factory,
        city_factory,
        option_factory,
        api_client
    ):
        city_slug = city_factory(slug="test-city-slug")
        option_slug = option_factory(slug="test-option-slug")
        cafe = cafe_factory(city=city_slug)
        cafe.options.add(option_slug)
        response = api_client().get(
            f"{self.endpoint}{city_slug.slug}/option-{option_slug.slug}/"
        )
        # Assert
        assert response.status_code == 200
        assert len(response.json()) == 1


# class TestReviewEndpoints:

#     endpoint = "/api/review/"

#     def test_return_all_reviews(self, review_factory, api_client):
#         # Arrange
#         review_factory.create_batch(10)
#         # Act
#         response = api_client().get(self.endpoint)
#         # Assert
#         assert response.status_code == 200
#         assert len(json.loads(response.content)) == 10


# class TestBusinessHoursEndpoints:

#     endpoint = "/api/businesshours/"

#     def test_return_all_businesshours(self, business_hours_factory, api_client):
#         # Arrange
#         business_hours_factory.create_batch(10)
#         # Act
#         response = api_client().get(self.endpoint)
#         # Assert
#         assert response.status_code == 200
#         assert len(json.loads(response.content)) == 10
