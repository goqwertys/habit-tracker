from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from habits.models import Habit
from habits.validators import RewardOrRelatedValidator, ExecutionTimeValidator, PleasantRelatedValidator, \
    PleasantHabitValidator, FrequencyValidator, RelatedPublicValidator, RelatedOwnerValidator


class RelatedHabitSerializer(ModelSerializer):
    """ Serializer for linked habit (read only) """
    class Meta:
        model = Habit
        fields = '__all__'


class HabitSerializer(ModelSerializer):
    """ Habit serializer """
    # For reading data
    related_habit = RelatedHabitSerializer(read_only=True)

    # For writing data
    related_habit_id = PrimaryKeyRelatedField(
        queryset=Habit.objects.all(),
        source='related_habit',
        write_only=True,
        allow_null=True
    )

    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            RewardOrRelatedValidator('is_pleasant', 'related_habit', 'reward'),
            ExecutionTimeValidator('execution_time'),
            PleasantRelatedValidator('related_habit'),
            PleasantHabitValidator('is_pleasant', 'reward', 'related_habit'),
            FrequencyValidator('frequency'),
            RelatedPublicValidator('related_habit', 'is_public'),
            RelatedOwnerValidator('related_habit', 'owner')
        ]
