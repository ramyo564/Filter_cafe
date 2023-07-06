from rest_framework.test import APITestCase

from cafes.models import BusinessHours, Cafe
from filters.models import BallotBox, Filter, FilterScore
from users.models import User


class TestUserSignup(APITestCase):
    URL = "/api/v1/user/signup/"

    def test_user_signup_1(self):
        response = self.client.post(
            self.URL,
            data={"username": "test1", "password": "123"},
        )
        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200.",
        )

    def test_user_signup_2(self):
        response = self.client.post(
            self.URL,
            data={"username": "test1", "password": "123"},
        )
        data = response.json()
        self.assertEqual(
            data["username"],
            "test1",
            "username이 잘못 출력되었습니다.",
        )

    def test_user_signup_3(self):
        response = self.client.post(
            self.URL,
            data={
                "username": "test1",
                "password": "123",
            },
        )
        data = response.json()
        self.assertEqual(
            data["name"],
            "이름",
            "name의 디폴트 값이 달라졌습니다.",
        )

    def test_user_signup_4(self):
        response = self.client.post(
            self.URL,
            data={
                "username": "test1",
                "password": "123",
                "name": "테스트네임",
            },
        )
        data = response.json()
        self.assertEqual(
            data["name"],
            "테스트네임",
            "name이 잘못 출력되었습니다.",
        )


class TestUserLogin(APITestCase):
    URL = "/api/v1/user/login/"

    def setUp(self):
        user = User.objects.create(
            username="testuser",
        )
        user.set_password("123")
        user.save()

    def test_user_login_1(self):
        response = self.client.post(
            self.URL,
            data={
                "username": "testuser",
                "password": "123",
            },
        )
        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200.",
        )

    def test_user_login_2(self):
        response = self.client.post(
            self.URL,
            data={
                "username": "testuser_bad",
                "password": "123",
            },
        )
        self.assertEqual(
            response.status_code,
            400,
            "status code isn't 400.",
        )

    def test_user_login_3(self):
        response = self.client.post(
            self.URL,
            data={
                "username": "testuser",
                "password": "123123",
            },
        )
        self.assertEqual(
            response.status_code,
            400,
            "status code isn't 400.",
        )


class TestUserLogout(APITestCase):
    URL = "/api/v1/user/logout/"

    def setUp(self):
        user = User.objects.create(
            username="testuser",
        )
        user.set_password("123")
        user.save()
        self.client.force_login(
            user,
        )

    def test_user_logout_1(self):
        response = self.client.post(
            self.URL,
        )
        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200.",
        )


class TestUserInformation(APITestCase):
    URL = "/api/v1/user/info/"

    def setUp(self):
        user = User.objects.create(
            username="testuser",
        )
        user.set_password("123")
        user.save()
        self.user = user

    def test_user_info_delete_1(self):
        response = self.client.delete(
            self.URL,
        )
        self.assertEqual(
            response.status_code,
            403,
            "status code isn't 403.",
        )

    def test_user_info_delete_2(self):
        self.client.force_login(
            self.user,
        )
        response = self.client.delete(
            self.URL,
        )
        self.assertEqual(
            response.status_code,
            204,
            "status code isn't 204.",
        )
