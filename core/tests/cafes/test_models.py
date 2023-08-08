import pytest

pytestmark = pytest.mark.django_db


class TestCafeModel:
    def test_str_method(self, cafe_factory):

        x = cafe_factory(name="test_category")

        assert x.__str__() == "test_category"


class TestBusinessDaysModel:
    def test_str_method(self, business_days_factory):

        time = business_days_factory(day="test_day")

        assert time.__str__() == "test_day"


class TestCafeOptionModel:
    def test_str_method(self, cafe_option_factory, cafe_factory, option_factory):

        cafe = cafe_factory(name="test_cafe")
        option = option_factory(name="test_option")
        result = cafe_option_factory(
            cafe=cafe, cafe_option=option, rating=1, sum_user=1, sum_rating=2
        )
        assert str(result) == "test_cafe - test_option - total user: 1\n- total rating: 2"


class TestCafeBusinessHoursModel:
    def test_str_method(self, cafe_option_factory, cafe_factory, option_factory):

        cafe = cafe_factory(name="test_cafe")
        option = option_factory(name="test_option")
        result = cafe_option_factory(
            cafe=cafe, cafe_option=option, rating=1, sum_user=1, sum_rating=2
        )

        assert str(result) == "test_cafe - test_option - total user: 1\n- total rating: 2"


class TestCafeReviewsModel:
    def test_str_method(self, cafe_factory, user_factory, cafe_reviews_factory):

        cafe = cafe_factory(name="test_cafe")
        user = user_factory(name="test_user")
        result = cafe_reviews_factory(
            cafe=cafe, user=user, cafe_reviews="test_cafe_reviews"
        )

        assert str(result) == "test_cafe - test_user - test_cafe_reviews"
