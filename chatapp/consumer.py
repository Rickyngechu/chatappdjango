import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Group, Chat
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get group name from URL
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        self.group_group_name = f'chat_{self.group_name}'

        # Join group
        await self.channel_layer.group_add(
            self.group_group_name,
            self.channel_name
        )

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': f'You are now connected to the group {self.group_name}'
        }))

    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(
            self.group_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = self.scope["user"]

        # Save message to the database
        group = Group.objects.get(name=self.group_name)
        chat = Chat.objects.create(sender=sender, group=group, content=message)

        # Broadcast message to group
        await self.channel_layer.group_send(
            self.group_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username
            }
        )

    # Receive message from group
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': f'{sender}: {message}'
        }))
