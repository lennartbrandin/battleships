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
        self.socket = websocket.WebSocketApp(
            f"ws{s}://{self.url}:{self.port}/?room={self.room}&name={self.name}",
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
                self.signals.phase.emit(data["phase"])
                match data["phase"]:
                    case "WAITING_FOR_PLAYERS":
                        pass
                    case "SETUP":
                        self.player.setEnemy(data["extra"]["enemy"])
                    case "IN_PROGRESS":
                        pass
                    case "GAME_OVER":
                        pass
            case "PLAYER_CHANGED":
                if data["name"] == self.name:
                    pass
                else:
                    pass
            case "SHIP_PLACED":
                self.signals.shipPlaced.emit(data["x"], data["y"], data["length"], data["direction"])
            case "SHOT_FIRED":
                self.signals.shotFired.emit(data["x"], data["y"], data["player"], data["result"])
                match data["result"]:
                    case "HIT":
                        pass
                    case "MISS":
                        pass
                    case "SUNK":
                        pass
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
        self.sendPlaceBoat(boat.x, boat.y, boat.length, boat.isVertical)

    def sendFireShot(self, x, y):
        self.sendAction("FIRE_SHOT", {"x": x, "y": y})


class WebsocketSignals(QObject):
    """Define the signals available from a running worker thread."""
    opened = pyqtSignal()
    phase = pyqtSignal(str)
    shipPlaced = pyqtSignal(int, int, int, str)
    shotFired = pyqtSignal(int, int, str, str)
    message = pyqtSignal(str)
    error = pyqtSignal(Exception)
    closed = pyqtSignal(int, str)

if __name__=="__main__":
    from PyQt6.QtCore import QThreadPool
    from PyQt6.QtWidgets import QApplication
    from game import game
    import sys
    app = QApplication(sys.argv)
    threadPool = QThreadPool()
    game = game()
    ws = websocketClient(game, "localhost", 8080, "test", "test")
    ws.signals.opened.connect(lambda: print("Opened"))
    ws.signals.message.connect(lambda message: print(message))
    ws.signals.error.connect(lambda e: print(e))
    ws.signals.closed.connect(lambda code, msg: print(code, msg))
    threadPool.start(ws)
    sys.exit(app.exec())