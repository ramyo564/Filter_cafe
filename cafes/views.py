from rest_framework import viewsets
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Cafe, Review, BusinessDays
from .serializers import CafeSerializer, ReviewSerializer, BusinessDaysSerializer
from rest_framework.decorators import action


class CafeViewSet(viewsets.ViewSet):
    '''
    A Viewset for viewing all cafes
    '''
    queryset = Cafe.objects.all()

    @extend_schema(responses=CafeSerializer)
    def list(self, request):
        serializer = CafeSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=["get"],
        detail=False,
        url_path=r"(?P<city_slug>[-\uAC00-\uD7A3\w]+)",
        url_name="all",
    )
    def list_cafe_by_city(self, request, city_slug=None):
        '''
        An endpoint to return cafes by city slug
        '''

        serializer = CafeSerializer(
            self.queryset.filter(city__slug=city_slug),
            many=True
        )
        return Response(serializer.data)

    @action(
        methods=["get"],
        detail=False,
        url_path=(
            r"(?P<city_slug>[-\uAC00-\uD7A3\w]+)/(?P<option_slugs>[-\uAC00-\uD7A3\w/]+/?)+"
        ),
        url_name="all",
    )
    def list_cafe_by_city_and_option(self, request, city_slug=None, option_slugs=None):
        '''
        An endpoint to return cafes by city slug and option slug
        '''
        city_slugs = [city_slug]
        option_slugs = option_slugs.split("/") if option_slugs else []

        queryset = self.queryset

        if city_slugs:
            queryset = queryset.filter(city__slug__in=city_slugs)

        if option_slugs:
            queryset = queryset.filter(options__slug__in=option_slugs)

        queryset = queryset.distinct()
        serializer = CafeSerializer(queryset, many=True)
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


class BusinessDaysViewSet(viewsets.ViewSet):
    '''
    A Viewset for viewing all BusinessDays
    '''
    queryset = BusinessDays.objects.all()

    @extend_schema(responses=BusinessDaysSerializer)
    def list(self, request):
        serializer = BusinessDaysSerializer(self.queryset, many=True)
        return Response(serializer.data)
