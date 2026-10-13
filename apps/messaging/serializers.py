from rest_framework import serializers
from .models import Message, MessageReadStatus


from rest_framework import serializers
from .models import Message, MessageReadStatus


class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.EmailField(source='sender.email', read_only=True)

    class Meta:
        model = Message
        fields = [
            'id',
            'sender',
            'sender_email',
            'room',
            'content',
            'file',
            'timestamp',
            'updated_at',
            'is_edited'
        ]
        read_only_fields = ['sender', 'timestamp', 'updated_at', 'is_edited']

    # 👇 ADD IT HERE
    def validate_room(self, room):
        user = self.context['request'].user

        if not room.members.filter(id=user.id).exists():
            raise serializers.ValidationError("You are not a member of this room.")

        return room

    def create(self, validated_data):
        request = self.context['request']
        return Message.objects.create(
            sender=request.user,
            **validated_data
        )


class MessageReadStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageReadStatus
        fields = ['id', 'message', 'user', 'read_at']
        read_only_fields = ['user', 'read_at']