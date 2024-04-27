from django.urls import path

from .musicviews import mainviews, userviews

urlpatterns = [
    path("", userviews.MyPiecesView.as_view(), name="index"),
    path("login", mainviews.login_user, name="login"),
    path("labels", userviews.LabelRegistrationView.as_view()),
    path("overview", userviews.OverviewView.as_view(), name="musicpieceoverview")
]
