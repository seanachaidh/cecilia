from django.contrib.auth.models import User
from ..models import Profile


def profile_exists_for_user(user_model: User) -> bool:
    return Profile.objects.filter(user=user_model).exists()


def find_or_create_profile(user_model: User) -> Profile:
    exists = profile_exists_for_user(user_model)
    if exists:
        return Profile.objects.filter(user=user_model)
    else:
        return create_new_profile_for_user(user_model)


def create_new_profile_for_user(user_model: User) -> Profile:
    profile = Profile.objects.create(user=user_model)
    return profile.save()

