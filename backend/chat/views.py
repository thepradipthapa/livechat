# chat/views.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Conversation, ConversationParticipant
from .serializers import ConversationSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class CreateOrGetChatView(APIView):
    """ View to create or get a one-on-one chat conversation between two users. """
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        other_user_id = request.data.get("user_id")

        if not other_user_id:
            return Response(
                {"error": "user_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if str(request.user.id) == str(other_user_id):
            return Response(
                {"error": "You cannot chat with yourself"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            other_user = User.objects.get(id=other_user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Find existing conversation
        conversations = Conversation.objects.filter(
            participants__user=request.user
        ).filter(
            participants__user=other_user
        ).distinct()

        if conversations.exists():
            conversation = conversations.first()
            serializer = ConversationSerializer(conversation)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Create new conversation
        conversation = Conversation.objects.create()

        ConversationParticipant.objects.create(
            conversation=conversation,
            user=request.user,
        )
        ConversationParticipant.objects.create(
            conversation=conversation,
            user=other_user,
        )

        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
