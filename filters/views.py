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


# Create your views here.
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
