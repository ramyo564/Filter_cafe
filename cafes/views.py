from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from filters.models import BallotBox, Filter, FilterScore
from filters.serializers import BallotBoxSerializer, FilterSerializer

from .models import BusinessHours, Cafe
from .serializers import BusinessHoursSerializer, CafeCreateSerializer, CafesSerializer


# Create your views here.
def index(request):
    """
    시작페이지

    하드 코딩으로 생각하고 있음.
    """
    pass


class CityCafes(APIView):
    def get(self, request, city):
        """
        도시에 해당하는 카페들이 나와야 됨.(status 200)
        카페가 2개가 있다면 2개가 출력되어야 됨.
        페이지네이션(이건 테스트 코드 아직 추가X, 논의 필요)
        """

        cafes = Cafe.objects.filter(city=city)
        serializer = CafesSerializer(cafes, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, city):
        """
        도시에 해당하는 카페들이 필터링 정보에 따라 나와야 됨.
        필터링 정보는 request.post.getlist("filters")를 통해서 전달이 됩니다.
        적용된 필터링 내용 알 수 있어야 합니다.
        이때 필터링 내용이 추가 될 때마다 필터링 색이 변해야 합니다.(토글 사용)


        ex) ["wifi", "sockets", "alcohol"]

        항상: 총 카페 갯수 전달이 되어야 합니다.(이 부분은 프론트와 상의를 해야 한다. )
        """

        cafes = Cafe.objects.filter(city=city)
        min_satisfaction_score = 50
        cafe_satisfaction_list = []
        filters = request.data.getlist("filters")
        dic_filter = dict()

        for cafe in cafes:
            # dic_filter 초기화
            for filter in filters:
                dic_filter[filter] = 0
                dic_filter[filter + "_count"] = 0

            # dic_filter에 필터의 총 점수, 총 유저수(아래에서 평균 계산하기 위해)
            for ballot_box in cafe.ballot_boxs.all():
                dic_filter[str(ballot_box.filter)] += (
                    ballot_box.users.count() * ballot_box.score.score
                )
                dic_filter[str(ballot_box.filter) + "_count"] += ballot_box.users.count()

            # 유저가 선택한 필터들에 대하여 min_satisfaction_score 이상인지 확인
            for filter_ in filters:
                if (
                    dic_filter[filter_] != 0
                    and dic_filter[filter_ + "_count"] != 0
                    and dic_filter[filter_] // dic_filter[filter_ + "_count"]
                    >= min_satisfaction_score
                ):
                    pass
                else:
                    break
            else:
                # 통과하면 유저에게 보여줌.
                cafe_satisfaction_list.append(cafe)
        serializer = CafesSerializer(cafe_satisfaction_list, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


# ALL CITIES
# 테코 0626 현재 X(넘김)
class CityList(APIView):
    def get(self, request):
        """
        도시 목록이 보여야 한다.
        for city in Cafe.CityChoices
            print(city[0])
        이게 되나 확인. 안되면 하드 코딩 혹은 상의
        """

        cities = []
        for city in Cafe.CityChoices:
            cities.append(city[0])
        return Response(cities, status.HTTP_200_OK)


# SUGGEST PLACES
class CreateCafe(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        get:
        로그인 유저만 올 수 있음.(비로그인 유저는 회원가입 창으로)
        주소 입력창을 보여준다.
        주소 입력창에 정보가 들어오면 거기에 해당하는 위치를 보여준다.
        주소 관련 사진을 선택한다. (이건 구글 API를 활용해야 할 거 같다.)
        이름 입력창
        => 화면 설계가 나오면 구체화
        """
        return Response(
            {"ok": "ok"},
            status=status.HTTP_200_OK,
        )

    @transaction.atomic(using="default")
    def post(self, request):
        """
        post:
        정보를 바탕으로 카페를 생성한다.
        해당 Cafe의 Filter랑 FilterScore에 맞게 BallotBox를 생성해야 한다.
        slug를 활용하여 이름으로 주소창을 생성한다.# ! (이거 아직 안함.)
        """

        # 트랜젝션을 사용하여 모두 수행되거나 안되거나 설계하였음.
        try:
            with transaction.atomic():
                # 영업시간  생성
                bhSerializer = BusinessHoursSerializer(data=request.data["business_hours"])
                if bhSerializer.is_valid():
                    bhSerializer.save()
                # cafe 생성
                cafeSerializer = CafeCreateSerializer(data=request.data)
                if cafeSerializer.is_valid():
                    # 생성한 영업시간 삽입해 준다.
                    business_hours = BusinessHours.objects.get(pk=bhSerializer.data["id"])
                    cafe = cafeSerializer.save(
                        business_hours=business_hours,
                    )
                    # BallotBox 생성(len(all_filter) * len(all_score) 만큼 필요하다.)
                    all_filter = Filter.objects.all()
                    all_score = FilterScore.objects.all()
                    for filter in all_filter:
                        for score in all_score:
                            BallotBox.objects.create(
                                cafe=cafe,
                                filter=filter,
                                score=score,
                            )
                    return Response(
                        {"ok": "ok"},
                        status=status.HTTP_201_CREATED,
                    )

        except:
            pass
        return Response({"message": "Error"}, status=status.HTTP_400_BAD_REQUEST)


class EditCafe(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Cafe.objects.get(pk=pk)
        except Cafe.DoesNotExist:
            raise NotFound

    def get(self, request, cafe_pk):
        """
        get:
        로그인 한 유저만 볼 수 있음
        페이지를 하드 코딩으로 작성할 생각(좋아요는 100점, 보통은 50점, 싫어요는 0점)
        유저가 투표를 했는지 BallotBox를 확인하여 알려줘야 한다.
        ex) wifi No 선택하면 wifi: 0 으로 와야 된다.
        """

        cafe = self.get_object(cafe_pk)
        # 유저가 선택한 필터 보여주기 위해
        ballot_box_list = []
        for ballot_box in cafe.ballot_boxs.all():
            if request.user in ballot_box.users.all():
                ballot_box_list.append(ballot_box)
        serializer = BallotBoxSerializer(
            ballot_box_list,
            many=True,
        )
        return Response(serializer.data, status.HTTP_200_OK)

    # 아직 제대로 테스트는 안함.
    @transaction.atomic(using="default")
    def put(self, request, cafe_pk):
        """
        BallotBox를 해당 유저의 기존의 정보를 지우고 바뀐 정보를 입력(설명이 애매하여 테스트 코드 참고해야 됨.)
        """

        cafe = self.get_object(cafe_pk)
        ballot_box_list = request.data.getlist("ballot_box_list")
        try:
            with transaction.atomic():
                # 기존의 투표한 내용 삭제
                for ballot_box in cafe.ballot_boxs.all():
                    if request.user in ballot_box.users.all():
                        ballot_box.users.remove(request.user)
                # 선택한 정보로 투표
                for ballot_box_pk in ballot_box_list:
                    ballot_box = BallotBox.objects.get(pk=ballot_box_pk)
                    ballot_box.users.add(request.user)
                return Response(
                    {"ok": "ok"},
                    status.HTTP_201_CREATED,
                )
        except:
            pass
        return Response({"message": "Error"}, status=status.HTTP_400_BAD_REQUEST)


def cafe_delete(request, cafe_pk):
    """
    검사??? 어떻게 해야지 못정함.

    delete요청인지 확인

    cafe_pk가 있는지 검사

    해당 PK에 해당하는 데이터 삭제

    (이때 데이터를 복구가능하게 할지 아니면 그냥 영구 삭제할지)

    리다일렉트 city_cafes
    """
    pass


# testcode 아직 안짬.
class CafeFilter(APIView):
    # 관리자 전용 페이지
    permission_classes = [IsAdminUser]

    def get(self, request):
        """
        form만 있으면 되지 않을까?
        일단 모르겠어 가지고 all_filter 출력하도록 설정.
        """
        all_filters = Filter.objects.all()
        serializer = FilterSerializer(
            all_filters,
            many=True,
        )
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        filterSerializer = FilterSerializer(data=request.data)
        if filterSerializer.is_valid():
            filterSerializer.save()
            return Response(
                filterSerializer.data,
                status=status.HTTP_201_CREATED,
            )

        return Response({"message": "Error"}, status=status.HTTP_400_BAD_REQUEST)


class CafeFilterDetail(APIView):
    # 관리자 전용 페이지
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return Filter.objects.get(pk=pk)
        except Filter.DoesNotExist:
            raise NotFound

    def get(self, request, filter_pk):
        """
        form만 있으면 되지 않을까?
        일단 모르겠어 가지고 all_filter 출력하도록 설정.
        """
        filter = self.get_object(filter_pk)
        serializer = FilterSerializer(filter)
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, filter_pk):
        filter = self.get_object(filter_pk)
        filterSerializer = FilterSerializer(
            filter,
            data=request.data,
            partial=True,
        )
        if filterSerializer.is_valid():
            filterSerializer.save()
            return Response(
                filterSerializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            filterSerializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, filter_pk):
        filter = self.get_object(filter_pk)
        filter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
