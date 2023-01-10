import websocket
import rel
import json
from game import game as class_game
from game import player as class_player
from board import board as class_board # Use toIndex() function
from boat import boat as class_boat
from PyQt6.QtCore import QObject, QThread

class server(QObject):
    """Establish a websocket communication with server and create a game"""
    def __init__(self, address, port, room, player):
        """Create Websocket"""
        self.address = address
        self.port = port
        self.room = room
        self.player = player
        self.enemy = class_player("Enemy", self.player.board.maxBoats, self.player.board.size, "?")
        self.game = class_game(self, player, self.enemy)
        self.start()

    def start(self):
        prefix = "ws" if self.address == "localhost" else "wss" # Use unsecure if hosting local
        self.ws = websocket.WebSocketApp(
            f"{prefix}://{self.address}:{self.port}/?room={self.room}&name={self.player.name}",
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )   
        # In case of connection loss, reconnect
        self.ws.run_forever(dispatcher=rel, reconnect=5)
        rel.signal(2, rel.abort)
        rel.dispatch()

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
        print("Opened connection")

    def on_message(self, ws, message):
        print(message)
        dict_message = json.loads(message)
        type = dict_message["type"]
        data = dict_message["data"]
        match type:
            case "GAME_PHASE_CHANGED":
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
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("Closed connection")
        print(f"Status code: {close_status_code}, Message: {close_msg}")

    def getPlayer(self):
        return self.player

    def getEnemy(self):
        return self.enemy

if __name__=="__main__":
    Server = server(
        address="localhost",
        port=8080,
        room="1",
        player=class_player(input("Enter your name: "), [0, 0, 4, 3, 2, 1], 10, "0")
    )
    # game = game(
    #     None,
    #     player("Player1"),
    #     player("Player2")
    # )
    # game.setupAuto()