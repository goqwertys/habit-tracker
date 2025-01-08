from celery import shared_task

from habits.models import Habit


@shared_task
def send_habit_notification(habit_id):
    try:
        habit = Habit.objects.get(id=habit_id)
        # services.send_notification(habit)
        print(f"Sending notification for habit: {habit.name}")
        print(f"Action: {habit.action}")
        print(f"Time: {habit.start_time}")
        print(f"Place: {habit.place}")
    except Habit.DoesNotExists:
        print(f'Habit with ID: {habit_id} does not exists')
