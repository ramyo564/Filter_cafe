from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cafe
from .serializers import CityCafesSerializer


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
        serializer = CityCafesSerializer(cafes, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, city):
        """
        ! 필터링이 제대로 되는지 테스트x(에러때문에)
        도시에 해당하는 카페들이 필터링 정보에 따라 나와야 됨.
        필터링 정보는 request.post.getlist("filters")를 통해서 전달이 됩니다.
        적용된 필터링 내용 알 수 있어야 합니다.
        이때 필터링 내용이 추가 될 때마다 필터링 색이 변해야 합니다.(토글 사용)

        필터링 할때 점수 따져야 하나???

        ex) ["wifi", "sockets", "alcohol"]

        항상: 총 카페 갯수 전달이 되어야 합니다.(이 부분은 프론트와 상의를 해야 한다. )
        """
        cafes = Cafe.objects.filter(city=city)
        # 50점 이상 필터들
        answer = []  # 변수명 마땅한 이름 생각 안나서 answer로 함
        filters = request.data.getlist("filters")
        dic_filter = dict()

        for c in cafes:
            for f in filters:
                dic_filter[f] = 0
                dic_filter[f + "_count"] = 0

            for b in c.ballot_boxs.all():
                dic_filter[str(b.filter)] += b.users.count() * b.score.score
                dic_filter[str(b.filter) + "_count"] += b.users.count()

            for f in filters:
                if (
                    dic_filter[f] != 0
                    and dic_filter[f + "_count"] != 0
                    and dic_filter[f] // dic_filter[f + "_count"]
                    >= 50  # 여기 50을 변수로 관리하고 싶은데. 마땅한 이름이 생각이 안난다.
                ):
                    pass
                else:
                    break
            else:
                answer.append(c)
        serializer = CityCafesSerializer(answer, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


# ALL CITIES
# 테코 0626 현재 X(넘김)
class CityList(APIView):
    def get(request):
        """
        도시 목록이 보여야 한다.
        for city in Cafe.CityChoices
            print(city[0])
        이게 되나 확인. 안되면 하드 코딩 혹은 상의
        """


# SUGGEST PLACES
class CreateCafe(APIView):
    def get(request):
        """
        get과 POST로 구분
        get:
        로그인 유저만 올 수 있음.(비로그인 유저는 회원가입 창으로)
        주소 입력창을 보여준다.
        주소 입력창에 정보가 들어오면 거기에 해당하는 위치를 보여준다.
        주소 관련 사진을 선택한다. (이건 구글 API를 활용해야 할 거 같다.)
        이름 입력창


        post:
        정보를 바탕으로 카페를 생성한다.
        slug를 활용하여 이름으로 주소창을 생성한다.
        해당 Cafe의 Filter랑 FilterScore에 맞게 BallotBox를 생성해야 한다.


        리다이렉트
        해당 카페 필터링 조건을 보여준다.(필터링 편집 페이지로 이동)

        """


def cafe_edit(request, cafe_slug):
    """
    get과 put로 구분
    get:
    로그인 한 유저만 볼 수 있음
    페이지를 하드 코딩으로 작성할 생각(좋아요는 100점, 보통은 50점, 싫어요는 0점)
    유저가 투표를 했는지 BallotBox를 확인하여 알려줘야 한다.
    ex) wifi No 선택하면 wifi: 0 으로 와야 된다.
    put:
    요청시 로그인을 안했으면 status 403
    BallotBox를 해당 유저의 기존의 정보를 지우고 바뀐 정보를 입력(설명이 애매하여 테스트 코드 참고해야 됨.)


    """

    pass


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
