import pytest


pytestmark = pytest.mark.django_db


class TestUserModel:
    def test_str_method(self, user_factory):

        x = user_factory(name="test_user")

        assert x.__str__() == "test_user"


class TestUserRatingModel:
    def test_str_method(self, cafe_option_factory, user_rating_factory, option_factory):
        option = option_factory(name="test_option")
        cafe_option = cafe_option_factory(cafe_option=option)
        user_rating = user_rating_factory(cafe_option=cafe_option, rating="5")

        expected_str = (
            f"{cafe_option.cafe.name} - {cafe_option.cafe_option.name} - "
            f"total user: {cafe_option.sum_user}\n"
            f"- total rating: {cafe_option.sum_rating} - {user_rating.rating}"
        )

        assert str(user_rating) == expected_str
