from rest_framework import serializers
from .models import Room, RoomMember
from apps.users.models import User


class RoomMemberSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = RoomMember
        fields = ['id', 'email', 'username', 'role', 'joined_at']


class RoomSerializer(serializers.ModelSerializer):
    members = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )

    room_members = RoomMemberSerializer(
        source='roommember_set',
        many=True,
        read_only=True
    )

    class Meta:
        model = Room
        fields = [
            'id',
            'name',
            'is_group', 
            'created_at',
            'members',
            'room_members'
        ]
        read_only_fields = ['created_at']

    def create(self, validated_data):
        members_data = validated_data.pop('members')
        request = self.context['request']

        room = Room.objects.create(**validated_data)

        # Add creator as admin
        RoomMember.objects.create(
            user=request.user,
            room=room,
            role='admin'
        )

        # Add other members
        users = User.objects.filter(id__in=members_data)

        for user in users:
            if user != request.user:
                RoomMember.objects.create(
                    user=user,
                    room=room,
                    role='member'
                )

        return room
    
class UpdateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['name', 'is_group']

class AddMembersSerializer(serializers.Serializer):
    members = serializers.ListField(
        child=serializers.IntegerField()
    )

    def validate_members(self, value):
        if not value:
            raise serializers.ValidationError("Members list cannot be empty")
        return value