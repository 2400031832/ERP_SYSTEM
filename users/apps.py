from django.apps import AppConfig
from django.conf import settings


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        if getattr(settings, 'IS_VERCEL', False):
            from django.contrib.auth.models import update_last_login
            from django.contrib.auth.signals import user_logged_in

            user_logged_in.disconnect(update_last_login)
