from django.urls import path
from .views import SendMessageView, RoomMessagesView, MarkMessageReadView

urlpatterns = [
    path('send/', SendMessageView.as_view(), name='send-message'),
    path('room/<int:room_id>/', RoomMessagesView.as_view(), name='room-messages'),
    path('read/<int:message_id>/', MarkMessageReadView.as_view(), name='mark-read'),
]