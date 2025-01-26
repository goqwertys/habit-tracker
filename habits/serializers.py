from datetime import timedelta

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


class DurationFieldInSeconds(serializers.DurationField):
    def to_representation(self, value):
        if not value:
            return None

        # Convert timedelta to a string of the format "HH:MM:SS"
        total_seconds = int(value.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def to_internal_value(self, data):
        # Parse a string of the format "HH:MM:SS" in timedelta
        try:
            parts = list(map(int, data.split(':')))
            if len(parts) == 3:
                return timedelta(hours=parts[0], minutes=parts[1], seconds=parts[2])
            elif len(parts) == 2:
                return timedelta(minutes=parts[0], seconds=parts[1])
            raise serializers.ValidationError("Invalid time format. Use 'HH:MM:SS' or 'MM:SS'")
        except (ValueError, TypeError):
            raise serializers.ValidationError("Invalid time format. Use numbers separated by colons")


class HabitSerializer(serializers.ModelSerializer):
    execution_time = DurationFieldInSeconds(
        help_text="Format: HH:MM:SS or MM:SS (eg: 00:02:00 for 2 minutes)"
    )
    # To read data
    related_habit = RelatedHabitSerializer(read_only=True)

    # To record data
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
