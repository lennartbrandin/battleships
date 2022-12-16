import websocket
import rel
import json
from game import *
class server:
    """Establish a websocket communication with server and create a game"""
    def __init__(self, address, port, room, name):
        """Create Websocket"""
        self.address = address
        self.port = port
        self.room = room
        self.player = player(name)
        self.game = game(self, player)
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

    def action(self, type, data):
        """Send action to server"""
        self.send({
            "type": type,
            "data": data
        })

    def sendPlaceBoat(self, boat):
        """Send place boat action to server"""
        direction = "VERTICAL" if boat.isVertical else "HORIZONTAL"
        self.action(
            type = "PLACE_SHIP",
            data = json.dumps({
                "x": boat.xPos,
                "y": boat.yPos,
                "length": boat.length,
                "direction": direction
            }))
        # TODO: Implement status return: true if successful
        

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
                        self.game.setup()
            case "PLAYER_CHANGED":
                pass
            case "SHOT_FIRED":
                pass
            case "SHIP_PLACED":
                pass
            case "ERROR":
                raise Exception(data["code"])

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("Closed connection")
        print(f"Status code: {close_status_code}, Message: {close_msg}")

    def getPlayer(self):
        return self.player

if __name__=="__main__":
    Server = server(
        address="localhost", # "battleships.lennardwalter.com",
        port=8080, # 443,
        room="default",
        name="Player1"
    )