# Structural process of the game
from board import board as classBoard
from player import player as classPlayer, enemy as classEnemy, ai as classAI
from PyQt6.QtCore import QThread, QThreadPool
from websocketClient import websocketClient
# from ui.gameMenu import gameMenu
from ui.mainMenu import mainMenu
from ui.graphics.boatImage import icons

class game():
    """Structural process of the game"""
    def __init__(self):
        self.players=[] # Track players for offline mode

        self.gameMenu = mainMenu(self) # Start ui

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
            player = classPlayer(self, self.gameDetails["name"], self.gameDetails["room"], '0')
            player.webSocket = websocketClientThread(player, self.gameDetails["address"], self.gameDetails["port"], player.roomName, player.name)
            player.server = player.webSocket.webSocketClient
            self.players.append(player)
        elif self.gameDetails["gameType"] == "offline":
            pass
        if not hasattr(self, "boatIcons"):
            self.boatIcons = iconGeneratorThread(self) # Generate boat icons in background
        else:
            print("Boat icons already generated")
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
        self.webSocketClient.signals.opened.connect(lambda: self.player.createPlaceholder())
        self.webSocketClient.signals.phase.connect(lambda data: self.player.setPhase(data))
        self.webSocketClient.signals.shipPlaced.connect(lambda x, y, length, direction: self.player.shipPlaced(x, y, length, direction == "VERTICAL"))
        self.webSocketClient.signals.playerChanged.connect(lambda player: self.player.playerChanged(player))
        self.webSocketClient.signals.shotFired.connect(lambda x, y, player, result, shipCoordinates: self.player.shotFired(x, y, player, result, shipCoordinates))
        self.webSocketClient.signals.message.connect(lambda message: print(message))
        self.webSocketClient.signals.gameError.connect(lambda e: self.player.websocketError(e))
        self.webSocketClient.signals.error.connect(lambda e: print(e))
        self.webSocketClient.signals.closed.connect(lambda code, msg: self.player.websocketClosed(code, msg))
        self.threadPool.start(self.webSocketClient)

class iconGeneratorThread(QThread):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.threadPool = QThreadPool().globalInstance()
        self.iconGenerator = icons(self.game)
        self.iconGenerator.signals.finished.connect(lambda: print("Icons generated"))
        self.threadPool.start(self.iconGenerator)

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    game = game()
    sys.exit(app.exec())