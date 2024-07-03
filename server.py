import asyncio
from bleak import BleakServer

def notification_handler(sender, data):
    print(f"Received message: {data}")
    if data == b'person_passed':
        print('passed')

async def main():
    server = BleakServer(notification_handler)
    await server.start()
    print(f"Server started and listening for connections")
    await server.wait_for_disconnect()
    print("Server stopped")

asyncio.run(main())
