from django.urls import path

from .musicviews import mainviews, userviews, downloader, adminviews, passwordviews

urlpatterns = [
    path("", userviews.MyPiecesView.as_view(), name="index"),
    path("admin", adminviews.show_admin_panel, name="admin"),
    path("admin/createuser", adminviews.add_user, name="creatuser"),
    path("login", mainviews.login_user, name="login"),
    path("logout", mainviews.logout_user, name="logout"),
    path("labels", userviews.LabelRegistrationView.as_view()),
    path("overview", userviews.OverviewView.as_view(), name="musicpieceoverview"),
    path("download", downloader.download_file, name="download"),
    path("download/<int:file_id>", downloader.download_specific_file, name="download_specific"),
    path("login/resetpassword", passwordviews.password_reset, name="reset_password"),
    path("login/resetpassword/<str:password_token>", passwordviews.password_reset_confirm, name="password_reset_confirm"),
]
