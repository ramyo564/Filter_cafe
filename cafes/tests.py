from rest_framework.test import APITestCase

from cafes.models import Cafe
from filters.models import BallotBox, Filter, FilterScore
from users.models import User

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
        )
        cafe2 = Cafe.objects.create(
            city="서울",
            name="test cafe 2",
            address="test cafe address",
            business_hours="test cafe business_hours",
            img="test cafe img",
        )
        cafe1.save()
        cafe2.save()

    def test_CityCafesGet_1(self):
        response = self.client.get(self.URL + "서울")
        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200.",
        )

    def test_CityCafesGet_2(self):
        response = self.client.get(self.URL + "서울")
        data = response.json()

        self.assertEqual(
            len(data),
            2,
            "CityCafes 출력 갯수가 잘못되었습니다.",
        )


class TestCityCafesPost(APITestCase):
    URL = "/api/v1/"

    def setUp(self):
        user1 = User.objects.create(
            username="testuser",
        )
        user1.set_password("123")
        user1.save()
        user2 = User.objects.create(
            username="testuser22",
        )
        user2.set_password("123")
        user2.save()

        cafe1 = Cafe.objects.create(
            city="서울",
            name="test cafe 1",
            address="test cafe address",
            business_hours="test cafe business_hours",
            img="test cafe img",
        )
        cafe2 = Cafe.objects.create(
            city="서울",
            name="test cafe 2",
            address="test cafe address",
            business_hours="test cafe business_hours",
            img="test cafe img",
        )
        cafe1.save()
        self.cafe1 = cafe1
        cafe2.save()
        filter1 = Filter.objects.create(
            option="option1",
            name="wifi1",
            img="img1",
        )
        filter2 = Filter.objects.create(
            option="option2",
            name="wifi2",
            img="img2",
        )
        filter1.save()
        filter2.save()
        self.filter1 = filter1
        self.filter2 = filter2
        filterscore100 = FilterScore.objects.create(score=100)
        filterscore30 = FilterScore.objects.create(score=30)
        filterscore100.save()
        filterscore30.save()
        balbox11100 = BallotBox.objects.create(
            cafe=cafe1,
            filter=filter1,
            score=filterscore100,
        )
        balbox110 = BallotBox.objects.create(
            cafe=cafe1,
            filter=filter1,
            score=filterscore30,
        )
        balbox12100 = BallotBox.objects.create(
            cafe=cafe1,
            filter=filter2,
            score=filterscore100,
        )
        balbox120 = BallotBox.objects.create(
            cafe=cafe1,
            filter=filter2,
            score=filterscore30,
        )
        balbox11100.users.add(user1)
        balbox11100.save()

        balbox110.users.add(user2)
        balbox110.save()

        balbox12100.users.add(user1)
        balbox12100.save()

        balbox120.save()

    def test_city_cafes_post_1(self):
        response = self.client.post(
            self.URL + "서울",
            data={
                "filters": [self.filter1, self.filter2],
            },
        )
        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200.",
        )

    def test_city_cafes_post_2(self):
        response = self.client.post(
            self.URL + "서울",
            data={
                "filters": [self.filter1, self.filter2],
            },
        )
        data = response.json()
        self.assertEqual(
            data,
            [
                {
                    "pk": 1,
                    "name": "test cafe 1",
                    "city": "서울",
                    "address": "test cafe address",
                    "business_hours": "test cafe business_hours",
                }
            ],
            "status code isn't 200.",
        )


class TestCityList(APITestCase):
    URL = "/api/v1/cities"

    def test_city_list_1(self):
        response = self.client.get(self.URL)
        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200.",
        )

    # 도시 출력 갯수가 맞는지 확인을 해야 하지만,
    # 도시수를 OptionChoices로 정하는 관계로
    # 테스트가 어려워서 따로 안만듬.
    def test_city_list_2(self):
        response = self.client.get(self.URL)
        data = response.json()
        self.assertEqual(
            type(data),
            type([]),
            "cities에 문제가 없는지 확인해 주세요.",
        )


class TestCreateCafe(APITestCase):
    URL = "/api/v1/create"

    def setUp(self):
        Filter.objects.create(
            option="option1",
            name="wifi1",
            img="img1",
        )
        Filter.objects.create(
            option="option2",
            name="wifi2",
            img="img2",
        )
        filterscore100 = FilterScore.objects.create(score=100)
        filterscore30 = FilterScore.objects.create(score=30)
        filterscore100.save()
        filterscore30.save()

    def test_create_cafe(self):
        response = self.client.post(
            self.URL,
            data={
                "name": "cafe 1",
                "city": "서울",
                "address": "address 1",
                "business_hours": "9~12",
            },
        )
        self.assertEqual(
            response.status_code,
            201,
            "status code isn't 201.",
        )
