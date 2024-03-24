from django.urls import path

from .musicviews import mainviews, userviews

urlpatterns = [
    path("", mainviews.index, name="index"),
    path("login", mainviews.login_user, name="login"),
    path("labels", userviews.LabelRegistrationView.as_view())
]
