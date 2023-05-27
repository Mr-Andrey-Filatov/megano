from django.urls import path

from authapp.views import ProfileView, ChangePasswordView, SetAvatarView

urlpatterns = [
    path("api/profile/", ProfileView.as_view()),
    path("api/profile/password/", ChangePasswordView.as_view()),
    path("api/profile/avatar/", SetAvatarView.as_view()),
]
