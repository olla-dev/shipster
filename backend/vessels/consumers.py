from channels.generic.websocket import AsyncJsonWebsocketConsumer

class VesselConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.model = 'vessels'

        await self.channel_layer.group_add(
            self.model, 
            self.channel_name
        )
        await self.accept()

        print("Connected!")
        self.send_json(
            {
                "type": "welcome_message",
                "message": "Hey there! You've successfully connected!",
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.model, self.channel_name)
        await self.close()

    async def location_update(self, event):
        print(event["data"])
        await self.send_json(content=event['data'])