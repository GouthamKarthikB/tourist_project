from django.urls import path
from .views import CreateChatRoomView, MessageListView

urlpatterns = [
    path("create-room/", CreateChatRoomView.as_view(), name="create-chat-room"),
    path("messages/<int:chat_room_id>/", MessageListView.as_view(), name="message-list"),
]
