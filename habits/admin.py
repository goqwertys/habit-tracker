from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        'owner',
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
        'owner',
        'place',
        'action',
        'reward'
    )
    ordering = ('id',)
