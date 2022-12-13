import websocket
import json
class Server:
    """Establish a websocket communication with server and manage the game"""
    def __init__(self, address="battleships.lennardwalter.com", port=443, room="default", name="default"):
        """Create Websocket"""
        self.address = address
        self.port = port
        self.room = room
        self.name = name
        self.ws = self.start()
        print(self.ws.recv())

    def start(self):
        ws = websocket.WebSocketApp(
            f"wss://{self.address}:{self.port}/?room={self.room}&name={self.name}",
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )   
        ws.run_forever()
        return ws

    def send(self, message):
        """Send message to server"""
        self.ws.send(json.dumps(message))

    def on_open(self, ws):
        print("Opened connection")

    def on_message(self, ws, message):
        dict_message = json.loads(message)
        print(dict_message)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("Closed connection")
        print(f"Status code: {close_status_code}, Message: {close_msg}")
    
if __name__ == "__main__":
    server = Server()
