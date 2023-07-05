from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
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
        페이지네이션(이건 테스트 코드 아직 추가X, 논의 필요)
        """

        cafes = Cafe.objects.filter(city=city)
        serializer = CafesSerializer(cafes, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, city):
        """
        총 카페 갯수 전달이 되어야 합니다.(이 부분은 프론트와 상의를 해야 한다. )
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
        cities = []
        for city in Cafe.CityChoices:
            cities.append(city[0])
        return Response(cities, status.HTTP_200_OK)


# SUGGEST PLACES
class CreateCafe(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
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

    @transaction.atomic(using="default")
    def put(self, request, cafe_pk):
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


class CafeDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Cafe.objects.get(pk=pk)
        except Cafe.DoesNotExist:
            raise NotFound

    def get(self, request, cafe_pk):
        cafe = self.get_object(cafe_pk)
        serializer = CafesSerializer(cafe)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 이건 필요한가? 일단 만들어 놓음.
    def put(self, request, cafe_pk):
        cafe = self.get_object(cafe_pk)
        serializer = CafesSerializer(
            cafe,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, cafe_pk):
        cafe = self.get_object(cafe_pk)
        cafe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
