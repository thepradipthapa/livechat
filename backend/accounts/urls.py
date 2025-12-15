from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("verify/", views.UserVerifyView.as_view(), name="verify"),
]