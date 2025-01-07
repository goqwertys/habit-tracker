from datetime import timedelta

from django.db import models

from users.models import User

NULLABLE = {
    'blank': True,
    'null': True
}


class Habit(models.Model):
    """ Habit model """
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='owner',
        **NULLABLE
    )
    place = models.CharField(
        max_length=100,
        verbose_name='Place',
        **NULLABLE
    )
    start_time = models.TimeField(
        verbose_name='Start time',
        help_text='Choose the time when you need to perform the habit',
        **NULLABLE
    )
    action = models.CharField(
        max_length=100,
        verbose_name='The action of habit',
        help_text='Specify the action of the habit',
        **NULLABLE
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name='A sign of a pleasant habit'
    )
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        verbose_name='Related habit',
        related_name='related_habits',
        **NULLABLE
    )
    frequency = models.PositiveSmallIntegerField(
        default=7,
        verbose_name="Frequency of habit execution per week",
        help_text="Specify the frequency of habit execution",
    )
    reward = models.CharField(
        verbose_name='Reward after completing a habit'
    )
    execution_time = models.DurationField(
        default=timedelta(seconds=120),
        verbose_name='Time to do the habit'
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name='Is habit public'
    )
    class Meta:
        verbose_name = 'Habit'
        verbose_name_plural = 'Habits'
