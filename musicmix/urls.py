from django.urls import path

from .musicviews import mainviews, userviews, downloader, adminviews, passwordviews

urlpatterns = [
    path("", userviews.MyPiecesView.as_view(), name="index"),
    path("admin", adminviews.show_admin_panel, name="admin"),
    path("admin/createuser", adminviews.add_user, name="creatuser"),
    path("admin/deleteuser/<int:user_id>", adminviews.remove_user, name="remove_user"),
    path("admin/createpiece", adminviews.add_piece, name="add_piece"),
    path("admin/deletepiece/<int:piece_id>", adminviews.delete_piece, name="delete_piece"),
    path("login", mainviews.login_user, name="login"),
    path("logout", mainviews.logout_user, name="logout"),
    path("labels", userviews.LabelRegistrationView.as_view()),
    path("labels/<str:label_type>/add", adminviews.add_label),
    path("overview", userviews.OverviewView.as_view(), name="musicpieceoverview"),
    path("download", downloader.download_file, name="download"),
    path("download/<int:file_id>", downloader.download_specific_file, name="download_specific"),
    path("login/resetpassword", passwordviews.password_reset, name="reset_password"),
    path("login/resetpassword/<str:password_token>", passwordviews.password_reset_confirm, name="password_reset_confirm"),
]
