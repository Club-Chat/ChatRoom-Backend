# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async

from apps.chat.models import Room, RoomMember
from apps.messaging.models import Message
from apps.messaging.serializers import MessageSerializer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"

        user = self.scope.get("user")

        if user and user.is_authenticated:
            is_member = await self.is_room_member(
                user,
                self.room_id
            )

            if is_member:
                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.accept()

                print(
                    f"✅ WebSocket connected for room "
                    f"{self.room_id} - User: {user.email}"
                )

                return

        print(
            f"❌ WebSocket connection rejected "
            f"for room {self.room_id}"
        )

        await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        print(
            f"❌ WebSocket disconnected "
            f"for room {self.room_id}"
        )

    
    async def receive(self, text_data):
        pass


    async def chat_message(self, event):
        try:
            await self.send(
                text_data=json.dumps(event["message"])
            )

            print(
                f"📤 Message sent to client: "
                f"{event['message'].get('id')}"
            )

        except Exception as e:
            print(f"Error sending message: {str(e)}")

    @database_sync_to_async
    def is_room_member(self, user, room_id):
        try:
            room = Room.objects.get(id=room_id)

            return RoomMember.objects.filter(
                user=user,
                room=room
            ).exists()

        except Room.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, user, room_id, content):
        room = Room.objects.get(id=room_id)

        message = Message.objects.create(
            sender=user,
            room=room,
            content=content
        )

        return message

    @database_sync_to_async
    def serialize_message(self, message):
        return MessageSerializer(message).data

    
    @database_sync_to_async
    def get_room(self, room_id):
        """Get room details"""
        try:
            return Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return None
        
    @database_sync_to_async
    def is_room_member(self, user, room_id):
        try:
            room = Room.objects.get(id=room_id)

            return RoomMember.objects.filter(
                user=user,
                room=room
            ).exists()

        except Room.DoesNotExist:
            return False