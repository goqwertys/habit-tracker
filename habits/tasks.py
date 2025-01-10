from datetime import datetime

from celery import shared_task

from habits import services
from habits.models import Habit


@shared_task
def send_habit_notification():
    """ Sends notification about habit """
    hour_now = datetime.now().hour
    minute_now = datetime.now().minute
    habits = Habit.objects.filter(start_time__hour=hour_now, start_time__minute=minute_now)
    for habit in habits:
        reward_or_related_habit = habit.reward if habit.reward else (
            habit.related_habit.name if habit.related_habit else "No reward or related habit")
        message = f'''Friendly reminder.
Your habit {habit.name}:
    Action: {habit.action},
    Place: {habit.place},
    Time: {habit.start_time}
    Reward or related habit: {reward_or_related_habit}
    Execution time: {habit.execution_time}
Good luck'''
        services.send_notification(message, habit.owner.tg_chat_id)
        print(f'{habit.owner} - {habit.action} - {habit.place} sent to {habit.owner} ({habit.owner.telegram_nickname})')
