from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from cafes.models import Cafe
from filters.models import BallotBox, Filter, FilterScore
from filters.serializers import FilterScoreSerializer, FilterSerializer


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

    @transaction.atomic(using="default")
    def post(self, request):
        try:
            with transaction.atomic():
                # Filter생성
                filterSerializer = FilterSerializer(data=request.data)
                if filterSerializer.is_valid():
                    filterSerializer.save()
                    # BallotBox 생성(이 부분 테스트 코드X, 작성법 모르겠음.)
                    filter = Filter.objects.get(pk=filterSerializer.data["pk"])
                    for cafe in Cafe.objects.all():
                        for score in FilterScore.objects.all():
                            BallotBox.objects.create(
                                cafe=cafe,
                                filter=filter,
                                score=score,
                            )
                    return Response(
                        filterSerializer.data,
                        status=status.HTTP_201_CREATED,
                    )
        except:
            pass
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


#################################################


class CafeFilterScore(APIView):
    # 관리자 전용 페이지
    permission_classes = [IsAdminUser]

    def get(self, request):
        """
        all_filter 출력하도록 설정.
        """
        all_filter_score = FilterScore.objects.all()
        serializer = FilterScoreSerializer(
            all_filter_score,
            many=True,
        )
        return Response(serializer.data, status.HTTP_200_OK)

    @transaction.atomic(using="default")
    def post(self, request):
        try:
            with transaction.atomic():
                # score생성
                filterScoreSerializer = FilterScoreSerializer(data=request.data)
                if filterScoreSerializer.is_valid():
                    filterScoreSerializer.save()
                    # BallotBox 생성(이 부분 테스트 코드X, 작성법 모르겠음.)
                    score = FilterScore.objects.get(pk=filterScoreSerializer.data["pk"])
                    for cafe in Cafe.objects.all():
                        for filter in Filter.objects.all():
                            BallotBox.objects.create(
                                cafe=cafe,
                                filter=filter,
                                score=score,
                            )
                    return Response(
                        filterScoreSerializer.data,
                        status=status.HTTP_201_CREATED,
                    )
        except:
            pass
        return Response({"message": "Error"}, status=status.HTTP_400_BAD_REQUEST)


class CafeFilterScoreDetail(APIView):
    # 관리자 전용 페이지
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return FilterScore.objects.get(pk=pk)
        except FilterScore.DoesNotExist:
            raise NotFound

    def get(self, request, filter_score_pk):
        """
        form만 있으면 되지 않을까?
        일단 모르겠어 가지고 all_filter 출력하도록 설정.
        """
        filterScore = self.get_object(filter_score_pk)
        serializer = FilterScoreSerializer(filterScore)
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, filter_score_pk):
        filterScore = self.get_object(filter_score_pk)
        filterScoreSerializer = FilterScoreSerializer(
            filterScore,
            data=request.data,
            partial=True,
        )
        if filterScoreSerializer.is_valid():
            filterScoreSerializer.save()
            return Response(
                filterScoreSerializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            filterScoreSerializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, filter_score_pk):
        filterScore = self.get_object(filter_score_pk)
        filterScore.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
