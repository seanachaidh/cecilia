from typing import Any
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        is_debug = settings.DEBUG
        user_exists = User.objects.filter(is_superuser=True).exists()
        if not user_exists and is_debug:
            # Als de superuser nog niet bestaat maken we die
            User.objects.create_superuser("tester", "test@test.com", "12345")
            self.stdout.write("Super user is aangemaakt", self.style.SUCCESS)
        else:
            self.stdout.write("Super user bestaat al of we zitten in productie", self.style.SUCCESS)
    