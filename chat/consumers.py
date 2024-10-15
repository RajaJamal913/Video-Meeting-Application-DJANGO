import json
from channels.generic.websocket import AsyncWebsocketConsumer

class VideoChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'video_chat_room'
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'send_sdp',
                'message': data['message']
            }
        )

    async def send_sdp(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))
