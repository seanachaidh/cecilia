from django.urls import path

from .musicviews import mainviews, userviews, downloader

urlpatterns = [
    path("", userviews.MyPiecesView.as_view(), name="index"),
    path("login", mainviews.login_user, name="login"),
    path("labels", userviews.LabelRegistrationView.as_view()),
    path("overview", userviews.OverviewView.as_view(), name="musicpieceoverview"),
    path("download", downloader.download_file, name="download"),
    path("download/<int:file_id>", downloader.download_specific_file, name="download_specific")
]
