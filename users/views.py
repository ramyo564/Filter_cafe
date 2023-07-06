import requests
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer


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
            # 현재 세션 방식 채택(JWT사용하고 싶으면 바꾸어도 됩니다:)
            login(request, user)
            return Response({"ok": "환영합니다!"})
        else:
            return Response(
                {"error": "아이디와 비밀번호를 확인해 주세요."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "안녕하가세요!"})


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

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 테스트 코드 없음.
class KakaoLogIn(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            access_token = requests.post(
                "https://kauth.kakao.com/oauth/token",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={
                    "grant_type": "authorization_code",
                    "client_id": "REST API",
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
            # 이메일 허용 안하면 돌려 보내기
            if kakao_account.get("email") == None:
                return Response(
                    {"message": "이메일을 허용해 주세요."}, status=status.HTTP_400_BAD_REQUEST
                )
            # 이메일 @ 이전까지 사용하도록(테스트 해 봐야함 07/06)
            else:
                username = kakao_account.get("email").split("@")[0]
            try:
                user = User.objects.get(username=username)
                # 테스트 완료 이후 주석 풀어 주세요.
                # login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    username=username,
                    name=profile.get("nickname"),
                    avatar=profile.get("profile_image_url"),
                )
                user.set_unusable_password()
                # 테스트 완료 이후 주석 풀어 주세요.
                # user.save()
                # login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
