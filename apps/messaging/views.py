from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Message, MessageReadStatus
from .serializers import MessageSerializer


class SendMessageView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_create(self, serializer):
        # Save message
        message = serializer.save()

        # Serialize saved message
        message_data = MessageSerializer(message).data

        # Broadcast to websocket group
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            f"chat_{message.room.id}",
            {
                "type": "chat_message",
                "message": message_data
            }
        )


class RoomMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs['room_id']

        return Message.objects.filter(
            room_id=room_id
        ).order_by('timestamp')


class MarkMessageReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, message_id):
        read_status, created = MessageReadStatus.objects.get_or_create(
            message_id=message_id,
            user=request.user
        )

        return Response(
            {"message": "Marked as read"},
            status=status.HTTP_200_OK
        )
