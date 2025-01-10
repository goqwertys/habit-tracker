from datetime import datetime

from celery import shared_task

from habits.models import Habit


@shared_task
def send_habit_notification():
    # try:
    #     habit = Habit.objects.get(id=habit_id)
    #     # services.send_notification(habit)
    #     print(f"Sending notification for habit: {habit.name}")
    #     print(f"Action: {habit.action}")
    #     print(f"Time: {habit.start_time}")
    #     print(f"Place: {habit.place}")
    # except Habit.DoesNotExists:
    #     print(f'Habit with ID: {habit_id} does not exists')
    hour_now = datetime.now().hour
    minute_now = datetime.now().minute
    habits = Habit.objects.filter(start_time__hour=hour_now, start_time__minute=minute_now)
    for habit in habits:
        print(f'{habit.owner} - {habit.action} - {habit.place}')
