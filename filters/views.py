from rest_framework import viewsets
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import City, Filter, Option
from .serializers import CitySerializer, FilterSerializer, OptionSerializer


class CityViewSet(viewsets.ViewSet):
    '''
    A Viewset for viewing all Cities
    '''
    queryset = City.objects.all()

    @extend_schema(responses=CitySerializer)
    def list(self, request):
        serializer = CitySerializer(self.queryset, many=True)
        return Response(serializer.data)


class FilterViewSet(viewsets.ViewSet):
    '''
    A Viewset for viewing all Filters
    '''
    queryset = Filter.objects.all()

    @extend_schema(responses=FilterSerializer)
    def list(self, request):
        serializer = FilterSerializer(self.queryset, many=True)
        return Response(serializer.data)


class OptionViewSet(viewsets.ViewSet):
    '''
    A Viewset for viewing all Options
    '''
    queryset = Option.objects.all()

    @extend_schema(responses=OptionSerializer)
    def list(self, request):
        serializer = OptionSerializer(self.queryset, many=True)
        return Response(serializer.data)
