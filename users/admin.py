from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'avatar',
        'telegram_nickname',
        'tg_chat_id'
    )
