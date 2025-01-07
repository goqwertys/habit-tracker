from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.serializers import HabitSerializer


class HabitViewSet(ModelViewSet):
    """ Habit CRUD """
    queryset = Habit.objects.all()
    serializer_class =HabitSerializer
    pagination_class = HabitPaginator

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.owner = self.request.user
        habit.save()
