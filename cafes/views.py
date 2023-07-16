from rest_framework import viewsets
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Cafe
from .serializers import CafeSerializer
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
        url_name="cafes-all",
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
            r"(?P<city_slug>[-\uAC00-\uD7A3\w]+)"
            r"/option/(?P<option_slugs>[-\uAC00-\uD7A3\w/]+/?)+"
        ),
        url_name="cafes-all_by_city_options",
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

    @action(
        methods=["get"],
        detail=False,
        url_path=(
            r"(?P<city_slug>[-\uAC00-\uD7A3\w]+)"
            r"/cafe/(?P<cafe_slug>[-\uAC00-\uD7A3\w/]+/?)+"
        ),
        url_name="cafes-all_by_city_cafe",
    )
    def list_cafe_by_city_and_cafe(self, request, city_slug=None, cafe_slug=None):
        '''
        An endpoint to return cafes by city slug and cafe slug
        '''
        city_slug = [city_slug]
        cafe_slug = cafe_slug.split("/") if cafe_slug else []

        queryset = self.queryset

        if city_slug:
            queryset = queryset.filter(city__slug__in=city_slug)

        if cafe_slug:
            queryset = queryset.filter(slug__in=cafe_slug)

        serializer = CafeSerializer(queryset, many=True)
        return Response(serializer.data)


# class ReviewViewSet(viewsets.ViewSet):
#     '''
#     A Viewset for viewing all Reviews
#     '''
#     queryset = Review.objects.all()

#     @extend_schema(responses=ReviewSerializer)
#     def list(self, request):
#         serializer = ReviewSerializer(self.queryset, many=True)
#         return Response(serializer.data)

#     @action(
#         methods=["get"],
#         detail=False,
#         url_path=(
#             r"(?P<city_slug>[-\uAC00-\uD7A3\w]+)"
#             r"/cafe/(?P<cafe_slug>[-\uAC00-\uD7A3\w/]+/?)+"
#         ),
#         url_name="reviews-all_by_cafe",
#     )
#     def list_cafe_by_city_and_cafe(self, request, city_slug=None, cafe_slug=None):
#         '''
#         An endpoint to return cafes by city slug and cafe slug
#         '''
#         city_slug = [city_slug]
#         cafe_slug = cafe_slug.split("/") if cafe_slug else []

#         queryset = self.queryset

#         if city_slug:
#             queryset = queryset.filter(city__slug__in=city_slug)

#         if cafe_slug:
#             queryset = queryset.filter(slug__in=cafe_slug)

#         serializer = CafeSerializer(queryset, many=True)
#         return Response(serializer.data)
