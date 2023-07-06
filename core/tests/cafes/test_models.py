import pytest

pytestmark = pytest.mark.django_db


class TestCafeModel:
    def test_str_method(self, cafe_factory):

        x = cafe_factory(name="test_category")

        assert x.__str__() == "test_category"


class TestReviewModel:
    def test_str_method(self, review_factory):

        x = review_factory(reviews="test_reviews")

        assert x.__str__() == "test_reviews"


class TestBusinessHoursModel:
    def test_str_method(self, business_hours_factory):

        object = business_hours_factory()
        expected_string = (
            "Monday: 09:00 - 23:00\n"
            "Tuesday: 09:00 - 23:00\n"
            "Wednesday: 09:00 - 23:00\n"
            "Thursday: 09:00 - 23:00\n"
            "Friday: 09:00 - 23:00\n"
            "Saturday: 09:00 - 23:00\n"
            "Sunday: 09:00 - 23:00"
        )

        assert object.__str__() == expected_string
