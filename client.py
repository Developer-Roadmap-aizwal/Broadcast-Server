import asyncio
import websockets

class BroadcastClient:
    def __init__(self):
        self.uri = "ws://127.0.0.1:8080"

    async def send_message(self, websocket, message):
        await websocket.send(message)
        print(f"Sent message: {message}")

    async def receive_messages(self, websocket):
        while True:
            try:
                message = await websocket.recv()
                print(f"Received message: {message}")
            except websockets.ConnectionClosed:
                break

    async def start(self):
        async with websockets.connect(self.uri) as websocket:
            send_task = asyncio.create_task(self.receive_messages(websocket))
            while True:
                message = input()
                await self.send_message(websocket, message)
    # async def send_messages(self):
    #     while True:
    #         message = input()
    #         await self.send_message(message)


if __name__ == "__main__":
    client = BroadcastClient()
    asyncio.run(client.start())