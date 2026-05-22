import json

from channels.generic.websocket import AsyncWebsocketConsumer


# =========================================
# BALANCE CONSUMER
# =========================================
class BalanceConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        if self.scope["user"].is_anonymous:
            await self.close()
            return

        self.group_name = f"user_{self.scope['user'].id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

        # USER ONLINE STATUS
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "user_status",
                "status": "online"
            }
        )

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # ==============================
    # BALANCE UPDATE
    # ==============================
    async def send_balance(self, event):

        await self.send(text_data=json.dumps({

            "type": "balance",

            "balance": event["balance"],

            "interest": event["interest"]
        }))

    # ==============================
    # SUPPORT MESSAGE
    # ==============================
    async def support_message(self, event):

        await self.send(text_data=json.dumps({

            "type": "support",

            "message": event["message"],

            "sender": event["sender"],

            "unread": event["unread"]
        }))

    # ==============================
    # USER STATUS
    # ==============================
    async def user_status(self, event):

        await self.send(text_data=json.dumps({

            "type": "status",

            "status": event["status"]
        }))
     # =====================
    # SUPPORT MESSAGE
    # =====================
    async def support_message(self, event):

        await self.send(
            text_data=json.dumps({
                "type": "support",

                "message":
                event["message"],

                "sender":
                event["sender"]
            })
        )

class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass