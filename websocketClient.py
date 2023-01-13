import websocket
import rel
import json
from game import game as class_game
from game import player as class_player
from boat import boat as class_boat
from PyQt6.QtCore import *

class websocketClient(QRunnable):
    """Establish websocket connection as a worker of mainWindow"""
    def __init__(self, address, port, room, player):
        """Create Websocket"""
        super().__init__()
        self.signals = websocketClientSignals() # Communicate game events with the mainWindow
        self.address = address
        self.port = port
        self.room = room
        self.player = player
        self.enemy = class_player("Enemy", self.player.board.maxBoats, self.player.board.size, "?")
        self.game = class_game(self, player, self.enemy)

    @pyqtSlot()
    def run(self):
        prefix = "ws" if self.address == "localhost" else "wss" # Use unsecure if hosting local
        self.ws = websocket.WebSocketApp(
            f"{prefix}://{self.address}:{self.port}/?room={self.room}&name={self.player.name}",
            on_open=self.signals.websocketOpened.emit(),
            on_error=self.on_error,
            on_message=lambda ws, message: self.signals.websocketMessage.emit(message), #self.on_message,
            on_close=self.signals.websocketClosed.emit()
        )   
        self.ws.run_forever()

    def send(self, message):
        """Send message to server"""
        self.ws.send(json.dumps(message))
        print(f"Sent: {json.dumps(message)}")

    def action(self, type, data):
        """Send action to server"""
        self.send({
            "type": type,
            "data": data
        })

    def sendPlaceBoat(self, boat):
        """Send place boat action to server"""
        direction = "VERTICAL" if boat.isVertical else "HORIZONTAL"
        x, y = boat.getIndexes()
        self.action(
            type = "PLACE_SHIP",
            data = {
                "x": x,
                "y": y,
                "length": boat.length,
                "direction": direction
            })

    def sendPlaceShot(self, x, y):
        """Send FIRE_SHOT action to the server"""
        self.action(
            type = "FIRE_SHOT",
            data = {
                "x": x,
                "y": y
            }
        )
        

    def on_open(self, ws):
        self.signals.websocketOpened.emit()
        print("Opened connection")

    def on_message(self, ws, message):
        self.signals.websocketMessage.emit(message)
        print(message)
        dict_message = json.loads(message)
        type = dict_message["type"]
        data = dict_message["data"]
        match type:
            case "GAME_PHASE_CHANGED":
                self.signals.GAME_PHASE_CHANGED.emit(data["phase"]) # Report event to mainWindow to update GUI
                match data["phase"]:
                    case "WAITING_FOR_PLAYERS":
                        print("Waiting for players")
                        # TODO: GUI display status
                        pass
                    case "SETUP":
                        self.game.players[0].enemy.setName(data["extra"]["enemy"])
                        self.game.setup() if False else self.game.setupAuto()
                    case "IN_PROGRESS":
                        pass
                    case "GAME_OVER":
                        print("Game over")
            case "PLAYER_CHANGED":
                if data["name"] == self.player.name:
                    self.game.playerTurn()
                else: 
                    pass
            case "SHOT_FIRED":
                isSelf = data["player"] == self.player.name # Is the shot fired by the instance's player?
                x, y = data["x"], data["y"]
                board = self.player.enemy.board if data["player"] == self.player.name else self.player.board
                match data["result"]:
                    # Determine board on which to place shot
                    case "HIT":
                        state = "X"
                    case "MISS":
                        state = "M"
                    case "SUNK":
                        state = "S"
                        if isSelf:
                            # If activePlayer is instance's player, place sunk boat on enemy's empty board
                            board.placeBoat(
                                class_boat(
                                    length = len(data["shipCoordinates"]),
                                    isVertical = True if data["shipCoordinates"][0][0] == data["shipCoordinates"][1][0] else False, # Boat is vertical if x1 == x2
                                    x = data["shipCoordinates"][0][0],
                                    y = data["shipCoordinates"][0][1],
                                    isDestroyed=True
                                )
                            )
                        else:
                            # If instance's boat was sunk, just place shoot normally, sinking it is handled automatically
                            state = "X"
                board.placeShot(x, y, state)
                if isSelf and data["result"] != "MISS":
                    self.game.playerTurn()

            case "SHIP_PLACED":
                pass
            case "ERROR":
                self.game.playerTurn() # Retry turn

    def on_error(self, ws, error):
        self.signals.websocketError.emit(str(error))
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        self.signals.websocketClosed.emit()
        print(f"Websocket closed. Status code: {close_status_code}, Message: {close_msg}")

    def getPlayer(self):
        return self.player

    def getEnemy(self):
        return self.enemy

class websocketClientSignals(QObject):
    """Signals to communicate with the mainWindow"""
    websocketOpened = pyqtSignal()
    GAME_PHASE_CHANGED = pyqtSignal(str) # Report Game phase
    websocketMessage = pyqtSignal(str)
    websocketError = pyqtSignal(str)
    websocketClosed = pyqtSignal()

if __name__=="__main__":
    Server = websocketClient(
        address="localhost",
        port=8080,
        room="1",
        player=class_player(input("Enter your name: "), [0, 0, 4, 3, 2, 1], 10, '0')
    )
    Server.run()
