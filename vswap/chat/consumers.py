# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model # ใช้ตัวนี้ดึง CustomUser
from .models import Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.my_user = self.scope["user"]
        
        if not self.my_user.is_authenticated:
            await self.close()
            return

        # ID ของคู่สนทนาที่เราจะคุยด้วย
        self.other_user_id = self.scope['url_route']['kwargs']['id']
        
        # สร้างชื่อห้องให้ Unique: เอา ID น้อย-มาก มาเรียงกัน
        # เช่น User 1 คุยกับ User 5 -> ห้อง chat_1_5
        user_ids = sorted([int(self.my_user.id), int(self.other_user_id)])
        self.room_group_name = f"chat_{user_ids[0]}_{user_ids[1]}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # บันทึกข้อมูล
        await self.save_message(self.my_user.id, self.other_user_id, message)

        # ส่งเข้ากลุ่ม
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': self.my_user.id
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id
        }))

    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, message):
        sender = User.objects.get(id=sender_id)
        receiver = User.objects.get(id=receiver_id)
        Message.objects.create(sender=sender, receiver=receiver, content=message)