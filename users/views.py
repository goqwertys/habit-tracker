from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.permissions import IsOwner
from users.serializers import UserUpdateSerializer, UserProfileSerializer, UserSerializer


class UserCreateAPIView(CreateAPIView):
    """ APIView for registration """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)


class UserProfileViewSet(ModelViewSet):
    """ User CRUD """
    queryset = User.objects.all()
    permission_classes = [IsOwner]

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update'):
            return UserUpdateSerializer
        return UserProfileSerializer
