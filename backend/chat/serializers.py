from rest_framework import serializers
from .models import Conversation, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['id', 'name', 'created_at']
        
        
class ChatUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name","email"]

    
class LatestMessageSerializer(serializers.ModelSerializer):
    sender = ChatUserSerializer()
    class Meta:
        model = Message
        fields = ["id", "content", "sender", "timestamp"]


class ConversationMetaSerializer(serializers.Serializer):
    latest_message = LatestMessageSerializer(allow_null=True)
    unread_count = serializers.IntegerField()


class ChatListSerializer(serializers.Serializer):
    conversation_id = serializers.UUIDField()
    user = ChatUserSerializer()
    conversation = ConversationMetaSerializer()
