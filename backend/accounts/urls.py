from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("verify/", views.UserVerifyView.as_view(), name="verify"),
    path("profile/", views.UserProfileView.as_view(), name="profile"),
    path("users/", views.UserListView.as_view(), name="users"),
    path("users/<int:id>/", views.UserRetrieveView.as_view(), name="user-detail"),
]