from django.db.models import Q
from rest_framework.decorators import action, permission_classes

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.serializers import HabitSerializer
from users.permissions import IsOwner


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
            return Habit.objects.filter(Q(owner=user) | Q(is_public=True))
        else:
            return Habit.objects.filter(is_public=True)

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
