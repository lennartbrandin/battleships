# Structural process of the game
from board import board as classBoard
from player import player as classPlayer, enemy as classEnemy, ai as classAI
from PyQt6.QtCore import QThread, QThreadPool
from websocketClient import websocketClient
from ui.mainWindow import gameMenu as mainWindow
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


    class boardBlueprint(classBoard):
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
            if len(self.player) > 0:
                self.error("Game already started")
                return
            else:
                self.player.append(classPlayer(self, self.gameDetails["name"], '0'))
                self.startWebsocketClient(self.gameDetails["address"], self.gameDetails["port"], self.gameDetails["room"], self.gameDetails["name"])
        elif self.gameDetails["gameType"] == "offline":
            pass
        pass

    def setPhase(self, phase):
        """Set the current phase"""
        if phase == "WAITING_FOR_PLAYER":
            pass
        elif phase == "SETUP":
            self.player[0].grid = grid(self.player[0])

    def shipPlaced(self, x, y, length, isVertical):
        self.player[0].board.placeBoat(x, y, length, isVertical)
        print(self.player[0].board)
        self.player[0].grid.player.board.update()

    def cleanup(self):
        """Reset the game"""
        self.server.socket.close()
        for player in self.player:
            player.grid.destroy()
        self.player=[]

    def error(self, message):
        print(f"Error: {message}")

    def startWebsocketClient(self, host, port, room, name):
        self.websocketClient=websocketClientThread(self, host, port, room, name)
        self.server=self.websocketClient.webSocketClient

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
        self.webSocketClient.signals.opened.connect(lambda: print("Websocket opened"))
        self.webSocketClient.signals.phase.connect(lambda phase: game.setPhase(phase))
        self.webSocketClient.signals.shipPlaced.connect(lambda x, y, length, direction: game.shipPlaced(x, y, length, direction == "VERTICAL"))
        self.webSocketClient.signals.message.connect(lambda message: print(message))
        self.webSocketClient.signals.error.connect(lambda e: game.cleanup())
        self.webSocketClient.signals.closed.connect(lambda code, msg: print(code, msg))
        self.threadPool.start(self.webSocketClient)

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    game = game()
    sys.exit(app.exec())