import asyncio
import websockets

class BroadcastServer:
    def __init__(self):
        self.connected_clients = set()
        self.lock = asyncio.Lock()

    async def register(self, websocket):
        self.connected_clients.add(websocket)
        print(f"Client connected: {websocket.remote_address}")

    async def broadcast(self, message):
        async with self.lock:
            for client in list(self.connected_clients):
                try:
                    await client.send(message)
                except Exception as e:
                    print(f"Error broadcasting to client: {e}")
                    await self.unregister(client)

    async def unregister(self, websocket):
        async with self.lock:
            self.connected_clients.remove(websocket)

    async def handle_client(self, websocket, path):
        await self.register(websocket)
        try:
            async for message in websocket:
                print(f"Received message: {message}")
                await self.broadcast(message)
        except websockets.ConnectionClosed:
            await self.unregister(websocket)

    async def start(self):
        async with websockets.serve(self.handle_client, "127.0.0.1", 8080):
            print("Server listening on port 8080")
            await asyncio.Future()


if __name__ == "__main__":
    server = BroadcastServer()
    asyncio.run(server.start())