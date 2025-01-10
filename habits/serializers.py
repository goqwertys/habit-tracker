from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from habits.models import Habit
from habits.validators import RewardOrRelatedValidator, ExecutionTimeValidator, PleasantRelatedValidator, \
    PleasantHabitValidator, FrequencyValidator, RelatedPublicValidator, RelatedOwnerValidator


class RelatedHabitSerializer(ModelSerializer):
    """ Serializer for linked habit (read only) """
    class Meta:
        model = Habit
        fields = '__all__'


class HabitSerializer(serializers.ModelSerializer):
    # Для чтения данных
    related_habit = RelatedHabitSerializer(read_only=True)

    # Для записи данных
    related_habit_id = serializers.PrimaryKeyRelatedField(
        queryset=Habit.objects.all(),
        source='related_habit',
        write_only=True,
        allow_null=True,
        default=None
    )

    class Meta:
        model = Habit
        fields = [
            'id', 'name', 'place', 'start_time', 'action', 'is_pleasant',
            'frequency', 'reward', 'execution_time', 'is_public', 'owner',
            'related_habit', 'related_habit_id'
        ]
        validators = [
            RewardOrRelatedValidator('is_pleasant', 'related_habit', 'reward'),
            ExecutionTimeValidator('execution_time'),
            PleasantRelatedValidator('related_habit'),
            PleasantHabitValidator('is_pleasant', 'reward', 'related_habit'),
            FrequencyValidator('frequency'),
            RelatedPublicValidator('related_habit', 'is_public'),
            RelatedOwnerValidator('related_habit', 'owner')
        ]
