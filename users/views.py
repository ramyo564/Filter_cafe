from rest_framework import viewsets
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ViewSet):
    '''
    A Viewset for viewing all Users
    '''
    queryset = User.objects.all()

    @extend_schema(responses=UserSerializer)
    def list(self, request):
        serializer = UserSerializer(self.queryset, many=True)
        return Response(serializer.data)
