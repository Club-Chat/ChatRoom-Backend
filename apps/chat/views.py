from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Room, RoomMember
from .serializers import AddMembersSerializer, RoomSerializer, UpdateRoomSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.users.models import User


class CreateRoomView(generics.CreateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}
    

class AddUserToRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        serializer = AddMembersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        room = Room.objects.get(pk=pk)

        # Optional: restrict to room members only
        if not RoomMember.objects.filter(room=room, user=request.user).exists():
            return Response({"error": "Not allowed"}, status=403)

        member_ids = serializer.validated_data['members']

        existing_user_ids = set(
            RoomMember.objects.filter(room=room).values_list('user_id', flat=True)
        )

        new_users = User.objects.filter(id__in=member_ids).exclude(id__in=existing_user_ids)

        new_members = [
            RoomMember(user=user, room=room, role='member')
            for user in new_users
        ]

        RoomMember.objects.bulk_create(new_members)

        return Response({
            "message": "Members added successfully"
        })


class UserRoomsView(generics.ListAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Room.objects.filter(members=self.request.user)


class RoomDetailView(generics.RetrieveAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Room.objects.filter(members=self.request.user)
    
class UpdateRoomView(generics.UpdateAPIView):
    serializer_class = UpdateRoomSerializer
    permission_classes = [IsAuthenticated]
    queryset = Room.objects.all()

    def get_queryset(self):
        # Only allow members to update
        return Room.objects.filter(members=self.request.user)
    
class DeleteRoomView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Room.objects.all()

    def get_queryset(self):
        # Optional: restrict only admin can delete
        return Room.objects.filter(members=self.request.user)