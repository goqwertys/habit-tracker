from rest_framework.serializers import ModelSerializer

from habits.models import Habit


class HabitSerializer(ModelSerializer):
    """ Habit serializer """
    class Meta:
        model = Habit
        fields = '__all__'
        validators = []
