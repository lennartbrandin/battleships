# Structural process of the game
from board import board as classBoard
from player import player as classPlayer, enemy as classEnemy, ai as classAI
from PyQt6.QtCore import QThread, QThreadPool
from websocketClient import websocketClient
from ui.gameMenu import gameMenu

class game():
    """Structural process of the game"""
    def __init__(self):
        super().__init__()
        self.players=[] # Track players for offline mode

        self.gameMenu = gameMenu(self) # Start ui

    def __str__(self):
        """Return game and its players as formatted string"""
        formattedString = f"{self.__class__.__name__}\n"
        for player in self.players:
            formattedString += f"{str(player)}\n"
        return formattedString

    class boardBlueprint(classBoard):
        """Create a board with game specific information"""
        def __init__(self, game, filler):
            """Extend the board class with game specific information"""
            self.game=game
            super().__init__(self.game.gameDetails["max boats"], self.game.gameDetails["board size"], filler)

    def startGame(self, gameDetails):
        """Create game"""
        self.gameDetails=gameDetails # Save details that were passed from the ui
        if self.gameDetails["gameType"] == "online":
            # Create player, enemies will be set up by the server
            player = classPlayer(self, self.gameDetails["name"], '0')
            server = websocketClientThread(player, self.gameDetails["address"], self.gameDetails["port"], self.gameDetails["room"], player.name)
            player.server = server.webSocketClient
            self.players.append(player)
        elif self.gameDetails["gameType"] == "offline":
            pass
        pass

    def autoSetup(self):
        """Setup the game automatically"""
        pass

    def play(self):
        """Play the game"""
        pass


class websocketClientThread(QThread):
    def __init__(self, *args):
        super().__init__()
        self.player = args[0]
        self.threadPool = QThreadPool().globalInstance()
        self.webSocketClient = websocketClient(*args)
        self.webSocketClient.signals.opened.connect(lambda: print("Websocket opened"))
        self.webSocketClient.signals.phase.connect(lambda phase: self.player.setPhase(phase))
        self.webSocketClient.signals.shipPlaced.connect(lambda x, y, length, direction: self.player.shipPlaced(x, y, length, direction == "VERTICAL"))
        self.webSocketClient.signals.shotFired.connect(lambda x, y, player, result: self.player.shotFired(x, y, player, result))
        self.webSocketClient.signals.message.connect(lambda message: print(message))
        self.webSocketClient.signals.error.connect(lambda e: print(e))
        self.webSocketClient.signals.closed.connect(lambda code, msg: print(msg))
        self.threadPool.start(self.webSocketClient)

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    game = game()
    sys.exit(app.exec())