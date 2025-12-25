from django.urls import path
from .views import CreateOrGetChatView

urlpatterns = [
    path("create/", CreateOrGetChatView.as_view()),
]
