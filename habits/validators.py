from dataclasses import fields
from datetime import timedelta

from rest_framework import serializers


class BaseValidator:
    """ Root class with init method """
    def __init__(self, *fields):
        self.fields = fields

    def __call__(self, attrs):
        """ The method that will be called by DRF for validation """
        field_values = {field: attrs.get(field) for field in self.fields}
        self.validate(**field_values)

    def validate(self, **kwargs):
        """ A method that must be implemented in child classes """
        raise NotImplementedError('Subclasses must implement this method.')


class RewardOrRelatedValidator(BaseValidator):
    """ Eliminates simultaneous selection of a related habit and reward """
    def validate(self, is_pleasant, related_habit, reward, **kwargs):
        if reward and related_habit:
            raise serializers.ValidationError(
                'A pleasant habit cannot have a related habit or reward.'
            )


class ExecutionTimeValidator(BaseValidator):
    """ Checks the execution time of a habit """
    def validate(self, execution_time, **kwargs):
        if execution_time and execution_time > timedelta(seconds=120):
            raise serializers.ValidationError(
                'The execution time should be no more than 120 seconds.'
            )


class PleasantRelatedValidator(BaseValidator):
    """ Only habits with the pleasant habit attribute can be included in related habits. """
    def validate(self, related_habit, **kwargs):
        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError(
                'The related habit must have the characteristic of a pleasant habit.'
            )


class PleasantHabitValidator(BaseValidator):
    """ A pleasant habit cannot have a reward or an related habit. """
    def validate(self, is_pleasant, reward, related_habit, **kwargs):
        if is_pleasant and (reward or related_habit):
            raise serializers.ValidationError(
                'A pleasant habit cannot have a reward or a related habit.'
            )


class FrequencyValidator(BaseValidator):
    """ Prohibits performing the habit less than once every 7 days """
    def validate(self, frequency, **kwargs):
        if frequency and not (1 <= frequency <= 7):
            raise serializers.ValidationError(
                'You cannot perform a habit less often than once every 7 days.'
            )
