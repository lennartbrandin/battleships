from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class gameMenu(QMainWindow):
    def __init__(self, game):
        super().__init__()
        self.setWindowTitle("Battleships")
        self.resize(800, 600)

        centralWidget = QWidget()
        self.main = self.mainLayout(game)
        centralWidget.setLayout(self.main)
        self.setCentralWidget(centralWidget)
        self.show()

    class mainLayout(QVBoxLayout):
        """Combine game detail prompts and game Type details"""
        def __init__(self, game):
            super().__init__()
            self.setSpacing(0)
            self.gameTypeDetails = self.gameTypeDetailsLayout(game)
            self.addLayout(self.gameTypeDetails)
            self.gameDetails = self.gameTypeDetails.gameDetails # Create a reference to the game details layout
            self.addLayout(self.gameDetails)

        class gameTypeDetailsLayout(QHBoxLayout):
            """Start game button and game type selector, responsible for updating the game details layout"""
            def __init__(self, game):
                super().__init__()
                self.game = game
                self.setSpacing(0)
                self.buttonStartGame = QPushButton("Start online game")
                self.selectorGameType = QComboBox()
                self.selectorGameType.addItems(["online", "offline"])
                self.addWidget(self.selectorGameType)
                self.addWidget(self.buttonStartGame)
                self.gameDetails = self.gameDetailsLayout()

                self.buttonStartGame.clicked.connect(lambda: self.game.startGame(self.gameDetails.details))
                self.selectorGameType.currentTextChanged.connect(lambda gameType: self.updateGameDetailsLayout(gameType))

            def updateGameDetailsLayout(self, gameType):
                """Update the game details layout based on the game type"""
                self.buttonStartGame.setText(f"Start {gameType} game")
                self.gameDetails.update(gameType)

            class gameDetailsLayout(QVBoxLayout):
                def __init__(self):
                    super().__init__()
                    self.setSpacing(0)
                    self.details = {}
                    self.defaultValues()
                    self.update(self.details["gameType"])

                def defaultValues(self):
                    """Set the default values for the game details"""
                    self.details["gameType"] = "online"

                    # Online game details
                    self.details["address"] = "battleships.lennardwalter.com"
                    self.details["port"] = "443"
                    self.details["room"] = "1"
                    self.details["name"] = "Player"

                    # Offline game details
                    self.details["board size"] = "10"
                    self.details["max boats"] = {str(k): str(v) for k, v in enumerate([0, 0, 4, 3, 2, 1])} # {"length": "amount"}
                    self.details["player amount"] = "2"

                def update(self, gameType):
                    """Update the game details layout based on the game type"""
                    self.details["gameType"] = gameType

                    # Delete all items in the layout
                    deleteItems(self)

                    # Add the correct items to the layout
                    def detailPrompt(label, dict=self.details):
                        layout = QHBoxLayout()
                        layout.addWidget(QLabel(f"{label}:"))
                        input = QLineEdit(dict[label.lower()])
                        input.textChanged.connect(lambda text: dict.update({label.lower(): text}))
                        layout.addWidget(input)
                        return layout

                    if gameType == "online":
                        [self.addLayout(detailPrompt(label)) for label in ["Address", "Port", "Room", "Name"]]
                    elif gameType == "offline":
                        [self.addLayout(detailPrompt(label)) for label in ["Board size", "Player amount"]]

                        maxBoats = QHBoxLayout()
                        [maxBoats.addLayout(detailPrompt(label, self.details["max boats"])) for label in self.details["max boats"]]

                    

def deleteItems(layout):
    """Delete all items in the layout"""
    if layout:
        while layout.count(): # Iterate as long as there are items in the layout
            child = layout.takeAt(0) # Remove the first item in the layout
            if child.widget():
                child.widget().deleteLater() # Delete the widget
                child.widget().setParent(None) # Remove the widget from the layout
            elif child.layout():
                deleteItems(child.layout()) # Delete items in the layout
            else:
                child.deleteLater()
                QObjectCleanupHandler().add(child)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    game = gameMenu()
    sys.exit(app.exec())