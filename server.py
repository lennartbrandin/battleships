import websocket
class Server:
    def __init__(self, address="localhost", port=8080):
        self.address = address
        self.port = port

    def start(self):
        ws = websocket.WebSocket()
