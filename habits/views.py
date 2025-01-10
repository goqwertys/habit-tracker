from django.db.models import Q
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.serializers import HabitSerializer
from users.permissions import IsOwner

@method_decorator(
    name='list',
    decorator=swagger_auto_schema(
        operation_description='Endpoint for accessing only public habits'
    ),
)
@method_decorator(
    name='retrieve',
    decorator=swagger_auto_schema(
        operation_description='Habit detail API view'
    )
)
@method_decorator(
    name='create',
    decorator=swagger_auto_schema(
        operation_description='Habit create API view'
    )
)
@method_decorator(
    name='update',
    decorator=swagger_auto_schema(
        operation_description='Habit update API view'
    )
)
@method_decorator(
    name='destroy',
    decorator=swagger_auto_schema(
        operation_description='Habit delete API view'
    )
)
@method_decorator(
    name='my_habits',
    decorator=swagger_auto_schema(
        operation_description='Endpoint for accessing only your habits'
    )
)
class HabitViewSet(ModelViewSet):
    """ Habit CRUD """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator

    def get_permissions(self):
        if self.action in ('create',):
            self.permission_classes = [IsAuthenticated]
        if self.action in ('update', 'partial_update', 'destroy',):
            self.permission_classes = [IsOwner, IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Habit.objects.filter(Q(owner=user) | Q(is_public=True)).order_by('id')
        else:
            return Habit.objects.filter(is_public=True).order_by('id')

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.owner = self.request.user
        habit.save()

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_habits(self, request):
        """ Endpoint for accessing only your habits """
        habits = Habit.objects.filter(owner=request.user)
        serializer = self.get_serializer(habits, many=True)
        return Response(serializer.data)
