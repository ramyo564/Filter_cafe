from rest_framework.test import APITestCase

from cafes.models import BusinessHours, Cafe
from filters.models import BallotBox, City, Filter, FilterScore
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
        businesshours1 = BusinessHours.objects.create(
            mon="09~18시간",
            tue="09~18시간",
            wed="09~18시간",
            thu="09~18시간",
            fri="09~18시간",
            sat="09~18시간",
            sun="09~18시간",
        )
        businesshours2 = BusinessHours.objects.create(
            mon="09~18시간",
            tue="09~18시간",
            wed="09~18시간",
            thu="09~18시간",
            fri="09~18시간",
            sat="09~18시간",
            sun="09~18시간",
        )
        seoul = City.objects.create(
            name="서울",
        )
        cafe1 = Cafe.objects.create(
            city=seoul,
            name="test cafe 1",
            address="test cafe address",
            business_hours=businesshours1,
            img="test cafe img",
        )
        cafe2 = Cafe.objects.create(
            city=seoul,
            name="test cafe 2",
            address="test cafe address",
            business_hours=businesshours2,
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
        seoul = City.objects.create(
            name="서울",
        )
        self.city = seoul
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
        businesshours1 = BusinessHours.objects.create(
            mon="09~18시간",
            tue="09~18시간",
            wed="09~18시간",
            thu="09~18시간",
            fri="09~18시간",
            sat="09~18시간",
            sun="09~18시간",
        )
        self.businesshours1 = businesshours1
        businesshours2 = BusinessHours.objects.create(
            mon="09~18시간",
            tue="09~18시간",
            wed="09~18시간",
            thu="09~18시간",
            fri="09~18시간",
            sat="09~18시간",
            sun="09~18시간",
        )
        cafe1 = Cafe.objects.create(
            city=seoul,
            name="test cafe 1",
            address="test cafe address",
            business_hours=businesshours1,
            img="test cafe img",
        )
        cafe2 = Cafe.objects.create(
            city=seoul,
            name="test cafe 2",
            address="test cafe address",
            business_hours=businesshours2,
            img="test cafe img",
        )
        cafe1.save()
        self.cafe1 = cafe1
        cafe2.save()
        filter1 = Filter.objects.create(
            # option="option1",
            # img="img1",
            name="wifi1",
        )
        filter2 = Filter.objects.create(
            # option="option2",
            # img="img2",
            name="wifi2",
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
                    "city": self.city.pk,
                    "address": "test cafe address",
                    "business_hours": {
                        "fri": self.businesshours1.fri,
                        "id": self.businesshours1.pk,
                        "mon": self.businesshours1.mon,
                        "sat": self.businesshours1.sat,
                        "sun": self.businesshours1.sun,
                        "thu": self.businesshours1.thu,
                        "tue": self.businesshours1.tue,
                        "wed": self.businesshours1.wed,
                    },
                }
            ],
            "만들어진 카페에 정보가 틀립니다.",
        )


class TestCityList(APITestCase):
    URL = "/api/v1/cities/"

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
    URL = "/api/v1/create/"

    def setUp(self):
        Filter.objects.create(
            # option="option1",
            # img="img1",
            name="wifi1",
        )
        Filter.objects.create(
            # option="option2",
            # img="img2",
            name="wifi2",
        )
        filterscore100 = FilterScore.objects.create(score=100)
        filterscore30 = FilterScore.objects.create(score=30)
        filterscore100.save()
        filterscore30.save()
        user1 = User.objects.create(
            username="testuser",
        )
        user1.set_password("123")
        user1.save()
        self.client.force_login(
            user1,
        )
        seoul = City.objects.create(
            name="서울",
        )
        self.city = seoul

    # ! 테스트 코드가 너무 적음.
    def test_create_cafe(self):
        response = self.client.post(
            self.URL,
            data={
                "name": "cafe 1",
                "city": "서울",
                "address": "address 1",
                "business_hours": {
                    "fri": "09~18시간",
                    "mon": "09~18시간",
                    "sat": "09~18시간",
                    "sun": "09~18시간",
                    "thu": "09~18시간",
                    "tue": "09~18시간",
                    "wed": "09~18시간",
                },
            },
            format="json",
        )
        self.assertEqual(
            response.status_code,
            201,
            "status code isn't 201.",
        )


class TestEditCafe(APITestCase):
    URL = "/api/v1/edit/"

    def setUp(self):
        user1 = User.objects.create(
            username="testuser",
        )
        user1.set_password("123")
        user1.save()
        self.user = user1
        user2 = User.objects.create(
            username="testuser22",
        )
        user2.set_password("123")
        user2.save()
        self.user2 = user2
        businesshours1 = BusinessHours.objects.create(
            mon="09~18시간",
            tue="09~18시간",
            wed="09~18시간",
            thu="09~18시간",
            fri="09~18시간",
            sat="09~18시간",
            sun="09~18시간",
        )
        self.businesshours1 = businesshours1
        seoul = City.objects.create(
            name="서울",
        )
        cafe1 = Cafe.objects.create(
            city=seoul,
            name="test cafe 1",
            address="test cafe address",
            business_hours=businesshours1,
            img="test cafe img",
        )
        cafe1.save()
        self.cafe1 = cafe1
        filter1 = Filter.objects.create(
            # option="option1",
            # img="img1",
            name="wifi1",
        )
        filter2 = Filter.objects.create(
            # option="option2",
            # img="img2",
            name="wifi2",
        )
        self.filter1 = filter1
        self.filter2 = filter2
        filterscore100 = FilterScore.objects.create(score=100)
        filterscore30 = FilterScore.objects.create(score=30)
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
        self.balbox = balbox11100
        balbox11100.save()

        balbox110.users.add(user2)
        balbox110.save()

        balbox12100.users.add(user1)
        balbox12100.save()

        balbox120.save()

    # 로그인 안한 상황
    def test_edit_cafe_get_1(self):
        response = self.client.get(
            self.URL + str(self.cafe1.pk),
        )
        self.assertEqual(
            response.status_code,
            403,
            "status code isn't 403.",
        )

    def test_edit_cafe_get_2(self):
        self.client.force_login(
            self.user,
        )
        response = self.client.get(
            self.URL + str(self.cafe1.pk),
        )
        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200.",
        )

    def test_edit_cafe_get_3(self):
        self.client.force_login(
            self.user,
        )
        response = self.client.get(
            self.URL + str(self.cafe1.pk),
        )
        data = response.json()
        self.assertEqual(
            len(data),
            2,
            "EditCafe get 출력 갯수가 잘못되었습니다.",
        )

    def test_edit_cafe_get_4(self):
        self.client.force_login(
            self.user2,
        )
        response = self.client.get(
            self.URL + str(self.cafe1.pk),
        )
        data = response.json()
        self.assertEqual(
            len(data),
            1,
            "EditCafe get 출력 갯수가 잘못되었습니다.",
        )

    def test_edit_cafe_put_1(self):
        response = self.client.put(
            self.URL + str(self.cafe1.pk),
            data={
                "ballot_box_list": [
                    self.balbox,
                ],
            },
        )

        self.assertEqual(
            response.status_code,
            403,
            "status code isn't 403.",
        )

    def test_edit_cafe_put_2(self):
        self.client.force_login(
            self.user2,
        )
        response = self.client.put(
            self.URL + str(self.cafe1.pk),
            data={
                "ballot_box_list": [
                    self.balbox.pk,
                ],
            },
        )
        self.assertEqual(
            response.status_code,
            201,
            "status code isn't 201.",
        )

    # def test_edit_cafe_put_1(self):
    #     self.client.force_login(
    #         self.user2,
    #     )
    #     response = self.client.put(
    #         self.URL + str(self.cafe1.pk),
    #     )
    #     data = response.json()
    #     print(data)
    #     self.assertEqual(
    #         len(data),
    #         1,
    #         "EditCafe get 출력 갯수가 잘못되었습니다.",
    #     )


class TestCafeDetail(APITestCase):
    URL = "/api/v1/detail/"

    def setUp(self):
        user1 = User.objects.create(
            username="testuser",
        )
        user1.set_password("123")
        user1.save()
        self.user1 = user1
        seoul = City.objects.create(
            name="서울",
        )
        businesshours1 = BusinessHours.objects.create(
            mon="09~18시간",
            tue="09~18시간",
            wed="09~18시간",
            thu="09~18시간",
            fri="09~18시간",
            sat="09~18시간",
            sun="09~18시간",
        )
        self.businesshours1 = businesshours1
        cafe1 = Cafe.objects.create(
            city=seoul,
            name="test cafe 1",
            address="test cafe address",
            business_hours=businesshours1,
            img="test cafe img",
        )
        self.cafe1 = cafe1

    def test_cafe_detail_get_1(self):
        response = self.client.get(
            self.URL + str(self.cafe1.pk),
        )
        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200.",
        )

    def test_cafe_detail_get_2(self):
        response = self.client.get(
            self.URL + str(self.cafe1.pk),
        )
        data = response.json()
        self.assertEqual(
            data["name"],
            "test cafe 1",
            "잘못된 정보를 가져왔습니다.",
        )

    def test_cafe_detail_put_1(self):
        response = self.client.put(
            self.URL + str(self.cafe1.pk),
            data={
                "name": "test cafe put",
            },
        )
        self.assertEqual(
            response.status_code,
            403,
            "status code isn't 403.",
        )

    def test_cafe_detail_put_2(self):
        self.client.force_login(
            self.user1,
        )
        response = self.client.put(
            self.URL + str(self.cafe1.pk),
            data={
                "name": "test cafe put",
            },
        )
        self.assertEqual(
            response.status_code,
            201,
            "status code isn't 201.",
        )

    def test_cafe_detail_put_3(self):
        self.client.force_login(
            self.user1,
        )
        response = self.client.put(
            self.URL + str(self.cafe1.pk),
            data={
                "name": "test cafe put",
            },
        )
        data = response.json()
        self.assertEqual(
            data["name"],
            "test cafe put",
            "잘못된 정보를 가져왔습니다.",
        )

    def test_cafe_detail_delete_1(self):
        response = self.client.delete(
            self.URL + str(self.cafe1.pk),
        )
        self.assertEqual(
            response.status_code,
            403,
            "status code isn't 403.",
        )

    def test_cafe_detail_delete_2(self):
        self.client.force_login(
            self.user1,
        )
        response = self.client.delete(
            self.URL + str(self.cafe1.pk),
        )
        self.assertEqual(
            response.status_code,
            204,
            "status code isn't 204.",
        )
