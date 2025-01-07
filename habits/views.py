from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.serializers import HabitSerializer
from users.permissions import IsOwner


class HabitViewSet(ModelViewSet):
    """ Habit CRUD """
    queryset = Habit.objects.all()
    serializer_class =HabitSerializer
    pagination_class = HabitPaginator

    def get_permissions(self):
        if self.action in ('retrieve', 'create', 'update', 'destroy',):
            self.permission_classes = [
                IsOwner, IsAuthenticated
            ]
        return super().get_permissions()

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.owner = self.request.user
        habit.save()
