from multipledispatch import dispatch
from boat import boat
import websocket
import json
from PyQt6.QtCore import QRunnable, pyqtSignal, pyqtSlot, QObject

class websocketClient(QRunnable):
    """Establish websocket connection and send/receive data as woker of threadpool"""
    def __init__(self, game, url, port, room, name):
        super().__init__()
        self.game = game
        self.url = url
        self.port = port
        self.room = room
        self.name = name
        self.signals = WebsocketSignals()
        

    @pyqtSlot()
    def run(self):
        """Start websocket connection"""
        s = "s" if self.port == 443 else "" # Use secure connection if port is 443
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
                match data["phase"]:
                    case "WAITING_FOR_PLAYERS":
                        pass
                    case "SETUP":
                        self.game.player[0].setEnemy(data["extra"]["enemy"])
                        self.signals.setup.emit()
                    case "IN_PROGRESS":
                        pass
                    case "GAME_OVER":
                        pass
            case "PLAYER_CHANGED":
                if data["player"] == self.name:
                    pass
                else:
                    pass
            case "SHIP_PLACED":
                pass
            case "SHOT_FIRED":
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
        self.send(json.dumps({"type": action, "data": data}))

    @dispatch(int, int, int, bool)
    def sendPlaceBoat(self, x, y, length, isVertical):
        direction = "VERTICAL" if isVertical else "HORIZONTAL"
        self.action("PLACE_SHIP", {"x": x, "y": y, "length": length, "direction": direction})

    @dispatch(boat)
    def sendPlaceBoat(self, boat):
        self.sendPlaceBoat(boat.x, boat.y, boat.length, boat.isVertical)

    def sendFireShot(self, x, y):
        self.action("FIRE_SHOT", {"x": x, "y": y})


class WebsocketSignals(QObject):
    """Define the signals available from a running worker thread."""
    opened = pyqtSignal()
    setup = pyqtSignal()
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