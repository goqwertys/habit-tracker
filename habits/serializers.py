from rest_framework.serializers import ModelSerializer

from habits.models import Habit
from habits.validators import RewardOrRelatedValidator, ExecutionTimeValidator, PleasantRelatedValidator, \
    PleasantHabitValidator, FrequencyValidator


class HabitSerializer(ModelSerializer):
    """ Habit serializer """
    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            RewardOrRelatedValidator('is_pleasant', 'related_habit', 'reward'),
            ExecutionTimeValidator('execution_time'),
            PleasantRelatedValidator('related_habit'),
            PleasantHabitValidator('is_pleasant', 'reward', 'related_habit'),
            FrequencyValidator('frequency')
        ]
