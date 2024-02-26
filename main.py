import asyncio
import json
import socket
from sydney import SydneyClient

sydney = SydneyClient()

async def handle_client(reader, writer):
    data = await reader.read(4096)
    message = data.decode()
    form_data = json.loads(message)
    prompt = form_data.get("prompt")
    if prompt == "!reset":
        await sydney.reset_conversation()
        response = "Conversation reset"
    elif prompt == "!exit":
        response = "Goodbye"
    else:
        responses = []
        async for response in sydney.ask_stream(prompt):
            responses.append(response)
        response = ''.join(responses)
    
    writer.write(response.encode())
    await writer.drain()
    writer.close()

async def main():
    server = await asyncio.start_server(
        handle_client, '127.0.0.1', 5000)

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
