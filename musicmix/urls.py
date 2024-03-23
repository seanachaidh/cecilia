from django.urls import path

from .musicviews import mainviews

urlpatterns = [
    path("", mainviews.index, name="index"),
    path("login", mainviews.login_user, name="login")
]
