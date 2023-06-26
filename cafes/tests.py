from rest_framework.test import APITestCase

from cafes.models import Cafe

"""
get
1) 도시에 해당하는 카페들이 나와야 됨.(status 200)
2) 카페가 2개가 있다면 2개가 출력되어야 됨.
페이지네이션(아직 구현 x)
"""


class TestCityCafesGet(APITestCase):
    URL = "/api/v1/"

    def setUp(self):
        cafe1 = Cafe.objects.create(
            city="서울",
            name="test cafe 1",
            address="test cafe address",
            business_hours="test cafe business_hours",
            img="test cafe img",
            map="test cafe map",
        )
        cafe2 = Cafe.objects.create(
            city="서울",
            name="test cafe 2",
            address="test cafe address",
            business_hours="test cafe business_hours",
            img="test cafe img",
            map="test cafe map",
        )
        cafe1.save()
        cafe2.save()

    def test_CityCafesGet_1(self):
        response = self.client.get(self.URL + "seoul")
        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200.",
        )

    def test_CityCafesGet_2(self):
        response = self.client.get(self.URL + "seoul")
        data = response.json()

        self.assertEqual(
            len(data),
            2,
            "CityCafes 출력 갯수가 잘못되었습니다.",
        )


"""

"""


class TestCityCafesGet(APITestCase):
    URL = "/api/v1/"
    pass
