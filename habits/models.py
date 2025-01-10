from datetime import timedelta

from django.db import models

from users.models import User

NULLABLE = {
    'blank': True,
    'null': True
}


class Habit(models.Model):
    """ Habit model """
    name = models.CharField(
        max_length=100,
        verbose_name='Name',
        **NULLABLE
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Owner',
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
        verbose_name='Reward after completing a habit',
        **NULLABLE
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

    def __str__(self):
        return f'{self.owner.name} - {self.action} - {self.place} - {self.start_time}'

    # def create_periodic_task(self):
    #     """ Creates a periodic task in Celery Beat to notify you of a habit. """
    #     hour = self.start_time.hour
    #     minute = self.start_time.minute
    #
    #     schedule, _ = CrontabSchedule.objects.get_or_create(
    #         minute=minute,
    #         hour=hour,
    #         day_of_week='*',
    #         day_of_month='*',
    #         month_of_year='*'
    #     )
    #
    #     task = PeriodicTask.objects.create(
    #         crontab=schedule,
    #         name=f'Habit reminder - {self.name}',
    #         task='habits.tasks.send_habit_notification',
    #         args=json.dumps([self.id]),
    #         enabled=True
    #     )
    #
    #     return task
    #
    # def save(self, *args, **kwargs):
    #     """ Override the save method to automatically create a task when you create a habit. """
    #     if self.pk:
    #         old_habit = Habit.objects.get(pk=self.pk)
    #         if old_habit.start_time != self.start_time:
    #             PeriodicTask.objects.filter(name=f'Habit reminder - {self.name}').delete()
    #             self.create_periodic_task()
    #         else:
    #             self.create_periodic_task()
    #     super().save(*args, **kwargs)
