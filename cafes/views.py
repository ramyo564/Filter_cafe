from rest_framework import viewsets
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Cafe, Review, BusinessHours
from .serializers import CafeSerializer, ReviewSerializer, BusinessHoursSerializer


class CafeViewSet(viewsets.ViewSet):
    '''
    A Viewset for viewing all cafes
    '''
    queryset = Cafe.objects.all()

    @extend_schema(responses=CafeSerializer)
    def list(self, request):
        serializer = CafeSerializer(self.queryset, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ViewSet):
    '''
    A Viewset for viewing all Reviews
    '''
    queryset = Review.objects.all()

    @extend_schema(responses=ReviewSerializer)
    def list(self, request):
        serializer = ReviewSerializer(self.queryset, many=True)
        return Response(serializer.data)


class BusinessHoursViewSet(viewsets.ViewSet):
    '''
    A Viewset for viewing all BusinessHours
    '''
    queryset = BusinessHours.objects.all()

    @extend_schema(responses=BusinessHoursSerializer)
    def list(self, request):
        serializer = BusinessHoursSerializer(self.queryset, many=True)
        return Response(serializer.data)

# def index(request):
#     """
#     하위 디렉토리(subdirectory)로 도시 이름

#     쿼리 매개 변수로 필터링 조건과 페이지 정보가 들어옴.

#     필터링 후 페이지에 맞는 최대 20개씩 카페 목록을 출력
#     """
#     pass


# def create(request):
#     """
#     로그인 했을 때만 가능

#     POST요청만 가능

#     데이터 파싱(post를 통해 온 데이터 사용할 수 있게 변환) 후
#     name, filler, address 정보 입력

#     owner는 토의 후 재수정 필요

#     카페 생성

#     렌더 해당 카페 페이지
#     """
#     pass


# def put(request, cafe_pk):
#     """
#     로그인 유저인지 검사

#     put 요청인지 확인(put은 수정할 때 주로 보내는 요청. POST랑 비슷하지만 구분해서 사용함.)

#     cafe_pk가 있는지 검사

#     데이터 파싱 후 내용 수정.

#     리다일렉트 해당 카페 페이지
#     """
#     pass


# def delete(request, cafe_pk):
#     """
#     로그인 유저인지 검사

#     delete요청인지 확인

#     cafe_pk가 있는지 검사

#     해당 PK에 해당하는 데이터 삭제

#     (이때 데이터를 복구가능하게 할지 아니면 그냥 영구 삭제할지)

#     리다일렉트 해당 카페 페이지
#     """
#     pass


# def like(request, cafe_pk):
#     """
#     로그인 유저인지 검사

#     cafe_pk가 있는지 검사

#     해당 유저(request.user)가 해당 카페(cafe_pk)에 좋아요 눌렸는지 여부

#     눌렸으면 like사라지고

#     안 눌렸으면 like생성.

#     비동기처리
#     return JsonResponse(context)
#     """
#     pass
