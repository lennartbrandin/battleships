from multipledispatch import dispatch
from boat import boat
import websocket
import json
from PyQt6.QtCore import QRunnable, pyqtSignal, pyqtSlot, QObject

class websocketClient(QRunnable):
    """Establish websocket connection and send/receive data as worker of threadpool"""
    def __init__(self, player, url, port, room, name):
        super().__init__()
        self.player = player
        self.url = url
        self.port = port
        self.room = room
        self.name = name
        self.signals = WebsocketSignals()
        

    @pyqtSlot()
    def run(self):
        """Start websocket connection"""
        s = "s" if self.port == "443" else "" # Use secure connection if port is 443
        address = f"ws{s}://{self.url}:{self.port}/?room={self.room}&name={self.name}"
        print(f"Connecting to {address}")
        self.socket = websocket.WebSocketApp(
            address,
            on_open=lambda ws: self.signals.opened.emit(),
            on_message=self.on_event,
            on_error=lambda ws, e: self.signals.error.emit(e),
            on_close=lambda ws, code, msg: self.signals.closed.emit(code, msg),
        )
        self.socket.run_forever()

    def on_event(self, ws, message):
        self.signals.message.emit(message)
        type = json.loads(message)["type"]
        data = json.loads(message)["data"]
        match type:
            case "GAME_PHASE_CHANGED":
                self.signals.phase.emit(data)
            case "PLAYER_CHANGED":
                    pass
            case "SHIP_PLACED":
                self.signals.shipPlaced.emit(data["x"], data["y"], data["length"], data["direction"])
            case "SHOT_FIRED":
                self.signals.shotFired.emit(data["x"], data["y"], data["player"], data["result"], data["shipCoordinates"])
            case "ERROR":
                pass

    def send(self, message):
        self.socket.send(message)

    def sendAction(self, action, data):
        print(f"Sent: {{\"type\": \"{action}\", \"data\": {data}}}")
        self.send(json.dumps({"type": action, "data": data}))

    @dispatch(int, int, int, str)
    def sendPlaceBoat(self, x, y, length, direction):
        self.sendAction("PLACE_SHIP", {"x": x, "y": y, "length": length, "direction": direction})

    @dispatch(boat)
    def sendPlaceBoat(self, boat):
        self.sendPlaceBoat(boat.x, boat.y, boat.length, "VERTICAL" if boat.isVertical else "HORIZONTAL")

    def sendFireShot(self, x, y):
        self.sendAction("FIRE_SHOT", {"x": x, "y": y})


class WebsocketSignals(QObject):
    """Define the signals available from a running worker thread."""
    opened = pyqtSignal()
    phase = pyqtSignal(dict)
    shipPlaced = pyqtSignal(int, int, int, str)
    shotFired = pyqtSignal(int, int, str, str, object)
    message = pyqtSignal(str)
    error = pyqtSignal(Exception)
    closed = pyqtSignal(int, str)