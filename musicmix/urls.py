from django.urls import path

import musicmix.musicviews.labelviews

from .musicviews import mainviews, userviews, downloader, adminviews, passwordviews

urlpatterns = [
    path("", userviews.MyPiecesView.as_view(), name="index"),
    path("admin", adminviews.show_admin_panel, name="admin"),
    path("admin/users", adminviews.show_users, name="users"),
    path("admin/labels", adminviews.show_labels, name="labels"),
    path("admin/pieces", adminviews.show_pieces, name="pieces"),
    path("admin/createuser", adminviews.add_user, name="creatuser"),
    path("admin/updateuser/<int:user_id>", adminviews.update_user, name="updateuser"),
    path("admin/deleteuser/<int:user_id>", adminviews.remove_user, name="remove_user"),
    path("admin/createpiece", adminviews.add_piece, name="add_piece"),
    path("admin/deletepiece/<int:piece_id>", adminviews.delete_piece, name="delete_piece"),
    path("admin/editpiece/<int:piece_id>", adminviews.edit_piece),
    path("login", mainviews.login_user, name="login"),
    path("logout", mainviews.logout_user, name="logout"),
    path("labels", musicmix.musicviews.labelviews.handle_labels, name="my_labels"),
    path("labels/delete/<int:label_id>", adminviews.remove_label, name="label_remove"),
    path("labels/<str:label_type>/add", adminviews.add_label),
    path("overview", userviews.OverviewView.as_view(), name="musicpieceoverview"),
    path("download", downloader.download_file, name="download"),
    path("download/<int:file_id>", downloader.download_specific_file, name="download_specific"),
    path("login/resetpassword", passwordviews.password_reset, name="reset_password"),
    path("login/resetpassword/<str:password_token>", passwordviews.password_reset_confirm, name="password_reset_confirm"),
]
