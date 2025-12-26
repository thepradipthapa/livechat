from django.urls import path
from .views import CreateOrGetChatView, GetAllChatsView, SendMessageView

urlpatterns = [
    path("create/", CreateOrGetChatView.as_view()),
    path("list/all/", GetAllChatsView.as_view()),
    path("message/send/", SendMessageView.as_view()),
]
