# chat/views.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Conversation, ConversationParticipant
from .serializers import ConversationSerializer, ChatListSerializer, LatestMessageSerializer,ChatUserSerializer
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


class GetAllChatsView(APIView):
    """ View to get all chat conversations for the authenticated user."""
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        conversations = Conversation.objects.filter(
            participants__user=user
        ).distinct()

        chat_list = []

        for convo in conversations:
            # Get other participant
            other_participant = convo.participants.exclude(user=user).first()
            other_user = other_participant.user if other_participant else None

            # Latest message
            latest_message = convo.messages.order_by("-timestamp").first()

            # Unread count
            unread_count = convo.messages.filter(
                receiver=user,
                is_read=False
            ).count()

            chat_list.append({
                "conversation_id": convo.id,
                "user": ChatUserSerializer(other_user).data,
                "conversation": {
                    "latest_message": (
                        LatestMessageSerializer(latest_message).data
                        if latest_message else None
                    ),
                    "unread_count": unread_count,
                },
            })

        serializer = ChatListSerializer(chat_list, many=True)
        return Response(serializer.data)

