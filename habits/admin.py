from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'get_owner_email',
        'place',
        'start_time',
        'action',
        'is_pleasant',
        'related_habit',
        'frequency',
        'reward',
        'execution_time',
        'is_public',
    )
    list_filter = (
        'is_pleasant',
        'is_public'
    )
    search_fields = (
        'name',
        'owner__email',
        'owner__telegram_nickname',
        'place',
        'action',
        'reward'
    )
    ordering = ('id',)
