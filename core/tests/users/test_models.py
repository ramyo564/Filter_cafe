import pytest


pytestmark = pytest.mark.django_db


class TestUserModel:
    def test_str_method(self, user_factory):

        x = user_factory(name="test_user")

        assert x.__str__() == "test_user"
