from fastapi import WebSocket, APIRouter, WebSocketDisconnect, Query
from . import manager

websockets_router = APIRouter(prefix="/ws", tags=["WebSockets"])

@websockets_router.websocket("/")
async def websocket_endpoint(websocket: WebSocket, email: str | None = Query(default=None)):
    await manager.connect(websocket, email)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@websockets_router.websocket("/tip")
async def websocket_tip(websocket: WebSocket):
    await websocket.accept()
    policy = (
        "Password must be 10-64 chars."
        "One upper letter."
        "One lowercase letter."
        "A digit and special char. "
        "Passphrase must contain 4 lowercase words."
    )
    await websocket.send_text(policy)
    await websocket.close()
