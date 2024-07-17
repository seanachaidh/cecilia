from django.contrib.auth.models import User

def is_superuser(user: User) -> bool:
    return user.is_superuser
