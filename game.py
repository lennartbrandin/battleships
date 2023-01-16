# Structural process of the game
from board import board
from player import player, enemy, ai
from PyQt6.QtCore import QThread, QThreadPool
from websocketClient import websocketClient
from ui.mainWindow import mainWindow
from ui.grid import grid

class game(QThread):
    """Structural process of the game"""
    def __init__(self, disableUI=False):
        super().__init__()
        self.player=[]
        # Default values will be used when starting online game
        self.size=10
        self.maxBoats=[0, 0, 4, 3, 2, 1]

        self.mainWindow=mainWindow(self) if not disableUI else None

    def __str__(self):
        """Return game and its players as formatted string"""
        formattedString = f"{self.__class__.__name__}\n"
        for player in self.player:
            formattedString += f"{str(player)}\n"
        return formattedString


    class boardBlueprint(board):
        # This class will be used by the players
        def __init__(self, game, filler):
            """Extend the board class with game specific information"""
            self.game=game
            super().__init__(self.game.maxBoats, self.game.size, filler)

    def startGame(self, gameDetails):
        """Start a game"""
        self.gameDetails=gameDetails
        if self.gameDetails["gameType"] == "online":
            # Create player, enemy's will be set up by the server
            self.player.append(player(self, self.gameDetails["player"], '0'))
            self.startWebsocketClient(self.gameDetails["server"], self.gameDetails["port"], self.gameDetails["room"], self.gameDetails["player"])
        elif self.gameDetails["gameType"] == "offline":
            for i, entry in enumerate(self.gameDetails["players"]):
                obj = player(self, entry["name"], '0') if entry["type"] == "player" else ai(self, entry["name"])
                obj.setEnemy(self.player[i-1]) # Set enemy to the previous player 
                [obj.setEnemy(enemy(self, entry["name"])) for entry in self.gameDetails["players"]] # Create all enemies for the player
                self.player.append(obj)


    def startWebsocketClient(self, host, port, room, name):
        self.websocketClient=websocketClientThread(self, host, port, room, name)
        self.server=self.websocketClient.webSocketClient

    def setup(self):
        """Setup the game"""
        for player in self.player:
            print(player)
            player.grid=grid(player)

    def autoSetup(self):
        """Setup the game automatically"""
        pass

    def play(self):
        """Play the game"""
        pass


class websocketClientThread(QThread):
    def __init__(self, *args):
        super().__init__()
        game = args[0]
        self.threadPool = QThreadPool().globalInstance()
        self.webSocketClient = websocketClient(*args)
        self.webSocketClient.signals.opened.connect(lambda: print("Opened"))
        self.webSocketClient.signals.setup.connect(lambda: game.setup())
        self.webSocketClient.signals.message.connect(lambda message: print(message))
        self.webSocketClient.signals.error.connect(lambda e: print(e))
        self.webSocketClient.signals.closed.connect(lambda code, msg: print(code, msg))
        self.threadPool.start(self.webSocketClient)

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    game = game()
    sys.exit(app.exec())