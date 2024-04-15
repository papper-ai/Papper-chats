from fastapi import FastAPI

from src.chats.router import chats_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello from chats_service"}


app.include_router(chats_router)
