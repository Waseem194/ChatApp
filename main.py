import os
import json
import redis
import socketio
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

# 1. Direct Redis Connection
# Use from_url for easier configuration
r = redis.from_url(redis_url, decode_responses=True)

# 2. Socket.IO Redis Manager
mgr = socketio.AsyncRedisManager(redis_url)
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*', client_manager=mgr)

app = FastAPI()
socket_app = socketio.ASGIApp(sio, app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

@app.get("/")
async def get():
    # Make sure index.html is inside a folder named 'templates'
    index_path = os.path.join(BASE_DIR, "templates", "index.html")
    return FileResponse(index_path)

@sio.on("connect")
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.on("join")
async def handle_join(sid, username):
    # SAVE TO REDIS: Store username using SID as the key
    r.set(f"user:{sid}", username)
    print(f"Redis Update: Saved user {username} for session {sid}")
    
    await sio.emit("user_status", {"user": username, "status": "online"})

@sio.on("chat_message")
async def handle_chat_message(sid, data):
    message = data.get("msg")
    
    # GET FROM REDIS: Retrieve the username we saved earlier
    sender_name = r.get(f"user:{sid}") or "Unknown"
    
    # SAVE TO REDIS: Store the message in a List called 'chat_log'
    chat_entry = json.dumps({"name": sender_name, "msg": message})
    r.rpush("chat_log", chat_entry)
    
    # Send to sender
    await sio.emit("response", {"name": "You", "msg": message, "type": "sent"}, to=sid)
    # Broadcast to all others
    await sio.emit("response", {"name": sender_name, "msg": message, "type": "received"}, skip_sid=sid)

@sio.on("disconnect")
async def disconnect(sid):
    # CLEANUP: Remove user key from Redis when they leave
    r.delete(f"user:{sid}")
    print(f"Redis Update: Deleted session {sid}")