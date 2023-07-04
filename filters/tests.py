from rest_framework.test import APITestCase

from filters.models import Filter, FilterScore
from users.models import User

# Create your tests here.


class TestFilter(APITestCase):
    URL = "/api/v1/filter/"

    def setUp(self):
        user_staff = User.objects.create(
            username="testuser",
            is_staff=True,
        )
        user_staff.set_password("123")
        user_staff.save()
        self.user_staff = user_staff

        user2 = User.objects.create(
            username="testuser2",
        )
        user2.set_password("123")
        user2.save()
        self.user2 = user2

    def test_filter_get_1(self):
        response = self.client.get(
            self.URL,
        )
        self.assertEqual(
            response.status_code,
            403,
            "status code isn't 403.",
        )

    def test_filter_get_2(self):
        self.client.force_login(
            self.user2,
        )
        response = self.client.get(
            self.URL,
        )
        self.assertEqual(
            response.status_code,
            403,
            "status code isn't 403.",
        )

    def test_filter_get_3(self):
        self.client.force_login(
            self.user_staff,
        )
        response = self.client.get(
            self.URL,
        )
        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200.",
        )

    def test_filter_get_4(self):
        total = 4
        for i in range(total):
            Filter.objects.create(
                name=("wifi" + str(i)),
            )

        self.client.force_login(
            self.user_staff,
        )
        response = self.client.get(
            self.URL,
        )
        data = response.json()
        self.assertEqual(
            len(data),
            total,
            "필터의 갯수를 잘못 출력하였습니다.",
        )

    def test_filter_name_duplicate_check(self):
        self.client.force_login(
            self.user_staff,
        )

        total = 4
        try:
            for i in range(total):
                Filter.objects.create(
                    name=("wifi"),
                )
            self.assertEqual(
                0,
                1,
                "wifi 이름이 중복 생성되었습니다. .",
            )
        except:
            self.assertEqual(
                0,
                0,
                "통과.",
            )

    def test_filter_post_1(self):
        self.client.force_login(
            self.user_staff,
        )
        response = self.client.post(
            self.URL,
            data={"name": "wifi_1"},
        )
        self.assertEqual(
            response.status_code,
            201,
            "status code isn't 201.",
        )

    def test_filter_post_2(self):
        self.client.force_login(
            self.user_staff,
        )
        response = self.client.post(
            self.URL,
            data={"name": "wifi_1"},
        )
        data = response.json()
        self.assertEqual(
            data["name"],
            "wifi_1",
            "필터의 이름이 잘못되었습니다.",
        )


class TestFilterDetail(APITestCase):
    URL = "/api/v1/filter/"

    def setUp(self):
        user_staff = User.objects.create(
            username="testuser",
            is_staff=True,
        )
        user_staff.set_password("123")
        user_staff.save()
        self.user_staff = user_staff

        user = User.objects.create(
            username="testuser_nomal",
        )
        user.set_password("123")
        user.save()
        self.user = user

        filter1 = Filter.objects.create(
            name=("wifi"),
        )
        self.filter1 = filter1

    def test_filter_detail_get_1(self):
        response = self.client.get(
            self.URL + str(self.filter1.pk),
        )
        self.assertEqual(
            response.status_code,
            403,
            "status code isn't 403.",
        )

    def test_filter_detail_get_2(self):
        self.client.force_login(
            self.user,
        )
        response = self.client.get(
            self.URL + str(self.filter1.pk),
        )
        self.assertEqual(
            response.status_code,
            403,
            "status code isn't 403.",
        )

    def test_filter_detail_get_3(self):
        self.client.force_login(
            self.user_staff,
        )
        response = self.client.get(
            self.URL + str(self.filter1.pk),
        )
        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200.",
        )

    def test_filter_detail_get_4(self):
        self.client.force_login(
            self.user_staff,
        )
        response = self.client.get(
            self.URL + str(self.filter1.pk),
        )
        data = response.json()
        self.assertEqual(
            data["name"],
            "wifi",
            "filter 이름이 잘못 출력되었습니다.",
        )

    def test_filter_detail_put_1(self):
        self.client.force_login(
            self.user_staff,
        )
        response = self.client.put(
            self.URL + str(self.filter1.pk),
            data={
                "name": "wifi_put",
            },
        )
        self.assertEqual(
            response.status_code,
            201,
            "filter 이름이 잘못 출력되었습니다.",
        )

    def test_filter_detail_put_2(self):
        self.client.force_login(
            self.user_staff,
        )
        response = self.client.put(
            self.URL + str(self.filter1.pk),
            data={
                "name": "wifi_put",
            },
        )
        data = response.json()
        self.assertEqual(
            data["name"],
            "wifi_put",
            "filter 이름이 잘못 수정되었습니다.",
        )

    def test_filter_detail_delete_1(self):
        self.client.force_login(
            self.user_staff,
        )
        response = self.client.delete(
            self.URL + str(self.filter1.pk),
        )
        self.assertEqual(
            response.status_code,
            204,
            "filter 삭제에 문제가 있습니다.",
        )
