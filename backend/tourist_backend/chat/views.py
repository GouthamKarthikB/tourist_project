from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer

class CreateChatRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user1 = request.user
        user2_id = request.data.get("user2_id")
        place_name = request.data.get("place_name")

        if not user2_id or not place_name:
            return Response({"error": "Missing user2_id or place_name"}, status=status.HTTP_400_BAD_REQUEST)

        user2 = get_object_or_404(User, id=user2_id)

        chat_room, created = ChatRoom.objects.get_or_create(user1=user1, user2=user2, place_name=place_name)
        
        return Response(ChatRoomSerializer(chat_room).data, status=status.HTTP_201_CREATED)

class MessageListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, chat_room_id):
        chat_room = get_object_or_404(ChatRoom, id=chat_room_id)
        messages = Message.objects.filter(chat_room=chat_room)
        return Response(MessageSerializer(messages, many=True).data)

    def post(self, request, chat_room_id):
        chat_room = get_object_or_404(ChatRoom, id=chat_room_id)
        data = request.data.copy()
        data["chat_room"] = chat_room.id
        data["sender"] = request.user.id
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
