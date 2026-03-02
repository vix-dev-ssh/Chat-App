import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Message
from asgiref.sync import sync_to_async
from django.utils import timezone

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):

    # async def connect(self):
    #     self.user = self.scope["user"]
    #     self.other_user_id = self.scope["url_route"]["kwargs"]["user_id"]

    #     if self.user.is_anonymous:
    #         await self.close()
    #     else:
    #         # Create unique room name
    #         users = sorted([str(self.user.id), str(self.other_user_id)])
    #         self.room_name = f"chat_{users[0]}_{users[1]}"
    #         self.room_group_name = self.room_name

    #         await self.channel_layer.group_add(
    #             self.room_group_name,
    #             self.channel_name
    #         )

    #         await self.accept()

    # async def connect(self):
    #     self.user = self.scope["user"]
    #     self.other_user_id = self.scope["url_route"]["kwargs"]["user_id"]

    #     if self.user.is_anonymous:
    #         await self.close()
    #     else:
    #         # Mark user online
    #         await self.set_user_online()

    #         users = sorted([str(self.user.id), str(self.other_user_id)])
    #         self.room_name = f"chat_{users[0]}_{users[1]}"
    #         self.room_group_name = self.room_name

    #         await self.channel_layer.group_add(
    #             self.room_group_name,
    #             self.channel_name
    #         )

    #         await self.accept()

    async def connect(self):
        #print("CONNECT CALLED")
        self.user = self.scope["user"]
        self.other_user_id = self.scope["url_route"]["kwargs"]["user_id"]

        if self.user.is_anonymous:
            await self.close()
        else:
            await self.set_user_online()

            users = sorted([str(self.user.id), str(self.other_user_id)])
            self.room_name = f"chat_{users[0]}_{users[1]}"
            self.room_group_name = self.room_name

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            # 🔥 Mark messages as read when user connects
            await self.mark_messages_as_read()

            await self.accept()

    # async def disconnect(self, close_code):
    #     await self.channel_layer.group_discard(
    #         self.room_group_name,
    #         self.channel_name
    #     )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        await self.set_user_offline()
    
    async def mark_messages_as_read(self):
        await sync_to_async(
            Message.objects.filter(
                sender_id=self.other_user_id,
                receiver_id=self.user.id,
                is_read=False
            ).update
        )(is_read=True)
    
    async def set_user_online(self):
        await sync_to_async(
            User.objects.filter(id=self.user.id).update
        )(is_online=True)
    
    # async def set_user_offline(self):
    #     self.user.is_online = False
    #     self.user.last_seen = timezone.now()
    #     await sync_to_async(self.user.save)()

    async def set_user_offline(self):
        await sync_to_async(
            User.objects.filter(id=self.user.id).update
        )(
            is_online=False,
            last_seen=timezone.now()
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]

        if message.strip() == "":
            return

        receiver = await sync_to_async(User.objects.get)(id=self.other_user_id)

        # Save message to DB
        await sync_to_async(Message.objects.create)(
            sender=self.user,
            receiver=receiver,
            content=message
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": self.user.username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
        }))
