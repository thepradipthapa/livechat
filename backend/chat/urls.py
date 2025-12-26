from django.urls import path
from .views import CreateOrGetChatView, GetAllChatsView

urlpatterns = [
    path("create/", CreateOrGetChatView.as_view()),
    path("list/all/", GetAllChatsView.as_view()),
]
