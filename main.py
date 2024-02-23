from fastapi import FastAPI, HTTPException, Request
import asyncio
from sydney import SydneyClient

app = FastAPI()
sydney = SydneyClient()

import asyncio
from sydney import SydneyClient

sydney = SydneyClient()

@app.post("/robot")
async def clientt(request:Request):
    async with SydneyClient() as sydney:
        form_data = await request.form()
        prompt = form_data.get("prompt")
        if prompt == "!reset":
            await sydney.reset_conversation()
            return "Conversation reset"
        elif prompt == "!exit":
            return "Goodbye"
        else:
            newp = prompt
            responses = []
            async for response in sydney.ask_stream(newp):
                responses.append(response)
            
            return ''.join(responses)

""" @app.post("/ask")
async def ask_sydney(request: Request):
    try:
        data = await request.json()
        print(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON data")

    prompt = await data.get("prompt")

    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt not provided")

    if prompt == "!reset":
        await sydney.reset_conversation()
        return {"response": "Conversation reset."}

    responses = await sydney.ask(prompt)
    return {"response": responses} """

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
