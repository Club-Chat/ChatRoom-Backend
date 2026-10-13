from django.urls import path
from .views import AddUserToRoomView, CreateRoomView, DeleteRoomView, UpdateRoomView, UserRoomsView, RoomDetailView


urlpatterns = [
    path('', UserRoomsView.as_view(), name='user-rooms'),
    path('create/', CreateRoomView.as_view(), name='create-room'),
    path('<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
    path('add-user/<int:pk>/', AddUserToRoomView.as_view(), name='add-user-to-room'),
    path('update/<int:pk>/', UpdateRoomView.as_view(), name='update-room'),
    path('delete/<int:pk>/', DeleteRoomView.as_view(), name='delete-room'),
]