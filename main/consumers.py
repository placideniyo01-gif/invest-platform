# main/consumers.py

import json

from channels.generic.websocket import AsyncWebsocketConsumer


class BalanceConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.group_name = "balance"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):

        pass

    async def send_balance(self, event):

        await self.send(text_data=json.dumps({

            "type":"balance",

            "balance":event["balance"],

            "interest":event["interest"]
        }))


class SupportConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.group_name = "support"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def support_message(self,event):

        await self.send(text_data=json.dumps({

            "type":"support",

            "message":event["message"]
        }))