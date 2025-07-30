from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.email_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, email: str | None = None):
        await websocket.accept()
        self.active_connections.append(websocket)
        if email:
            self.email_connections[email] = websocket

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        for key, ws in list(self.email_connections.items()):
            if ws is websocket:
                del self.email_connections[key]

    async def send_personal_message(self, message: str, email: str):
        websocket = self.email_connections.get(email)
        if websocket:
            await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
