import requests
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer


# 3 join community
class Signup(APIView):
    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError
        serializer = UserSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = UserSerializer(user)
            # 현재 세션 방식 채택(JWT사용하고 싶으면 바꾸어도 됩니다:)
            login(request, user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogIn(APIView):
    """
    로그인
    """

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            # login시키고 백엔드에 세션 생성, 사용자에게 cookie제공
            login(request, user)
            return Response({"ok": "Welcome!"})
        else:
            return Response(
                {"error": "wrong password"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LogOut(APIView):
    """
    로그 아웃
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "bye!"})


class UserInformation(APIView):
    permission_classes = [IsAuthenticated]

    def get(request):
        """
        프로필 페이지 구성

        뭘 작성해야 될지 모르겠어 가지고
        화면 나온 이후 할 예정
        """

    def put(request):
        """
        유저 정보 수정
        """

    def delete(request):
        """
        회원 탈퇴
        """


class KakaoLogIn(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            access_token = requests.post(
                "https://kauth.kakao.com/oauth/token",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={
                    "grant_type": "authorization_code",
                    "client_id": "0999329903a4ff2d986c09fdd71eb44f",
                    "redirect_uri": "http://127.0.0.1:3000/social/kakao",
                    "code": code,
                },
            )
            access_token = access_token.json().get("access_token")
            user_data = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                },
            )
            user_data = user_data.json()
            kakao_account = user_data.get("kakao_account")
            profile = kakao_account.get("profile")
            try:
                user = User.objects.get(email=kakao_account.get("email"))
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    email=kakao_account.get("email"),
                    username=profile.get("nickname"),
                    name=profile.get("nickname"),
                    avatar=profile.get("profile_image_url"),
                )
                user.set_unusable_password()
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
