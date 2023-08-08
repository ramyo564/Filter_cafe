import pytest


pytestmark = pytest.mark.django_db


class TestCafeEndpoints:

    endpoint = "/api/cafe/"

    def test_return_all_cafes(self, cafe_factory, api_client):

        cafe_factory.create_batch(10)
        response = api_client().get(path=self.endpoint)
        assert response.status_code == 200
        assert len(response.json()) == 10

    def test_return_all_cafes_by_city(self, cafe_factory, city_factory, api_client):
        city_slug = city_factory(slug="서울")
        cafe_factory(city=city_slug)
        response = api_client().get(f"{self.endpoint}{city_slug.slug}/")
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_return_all_cafes_by_city_option(
        self,
        cafe_factory,
        city_factory,
        cafe_option_factory,
        api_client
    ):
        city_slug = city_factory(slug="test-city-slug")
        cafe_option = cafe_option_factory().cafe_option
        cafe = cafe_factory(city=city_slug, slug="test-cafe-slug")
        cafe.options.add(cafe_option)
        response = api_client().get(
            f"{self.endpoint}{city_slug.slug}/option/{cafe_option.slug}/"
        )
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_return_all_cafes_by_city_cafe(
        self,
        cafe_factory,
        city_factory,
        api_client
    ):
        city_slug = city_factory(slug="test-city-slug")
        cafe = cafe_factory(city=city_slug, slug="test-cafe-slug")
        response = api_client().get(
            f"{self.endpoint}{city_slug.slug}/cafe/{cafe.slug}/"
        )
        assert response.status_code == 200
        assert len(response.json()) == 1
