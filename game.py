from board import board as class_board
from boat import boat as class_boat
import random

class player:
    """Create a player"""
    def __init__(self, name):
        """Create a board for the player"""
        self.name = name
        self.board = class_board(
            maxBoats=[0, 0, 4, 3, 2, 1], # List of maximum boats per length (0, 1, 2, 3, 4, 5)
            size=10 # Size of the board
        )

    def __str__(self):
        """Return a formatted string of own and enemy board besides each other"""
        formattedString = f"{self.name}'s board:"
        formattedString += " " * (22-len(formattedString)) # Add spaces to align the notation to the boards
        formattedString += f"{self.enemy.name}'s board:\n"
        for y in range(self.board.size):
            for x in range(self.board.size + 1 + self.enemy.getBoard().size): # +1 for the seperator
                if x < self.board.size:
                    formattedString += str(self.getBoard().getState(x,y)) + " "
                elif self.board.size <= x < self.board.size + 1:
                    formattedString += "| "
                elif self.board.size < x:
                    formattedString += str(self.enemy.getBoard().getState(x-self.enemy.getBoard().size-1,y)) + " "
            formattedString += "\n"
        return formattedString

    def getBoard(self):
        """Return the board of the player"""
        return self.board

    def setEnemy(self, player):
        """Set the enemy of the player"""
        self.enemy = player

    def setName(self, name):
        """Set the name of the player"""
        self.name = name

class game:
    def __init__(self, server, *players):
        self.server = server
        self.players = players if server == None else [server.getPlayer(), server.getEnemy()] # If playing online, copy the player names from the server
        self.activePlayerID = 0
        self.setEnemies()
    
    def __str__(self):
        return "\n".join([str(player) for player in self.players])

    def setEnemies(self):
        """Set the enemy of a player to the previous player"""
        for i, player in enumerate(self.players):
            player.setEnemy(self.players[i-1])

    def setup(self):
        """Setup the game"""
        # Place boat as long as the sum of existing boats is smaller than the sum of maximum boats
        for player in self.players:
            existingBoats = player.getBoard().boats # List of list of boat objects differed by length of boat
            maxBoats = player.getBoard().maxBoats # List of maximum boats per length
            amountOfBoats = [len(amount) for amount in existingBoats] # List of boat amounts differed by length of boat
            remainingBoats = [maxBoats[i] - amountOfBoats[i] for i in range(len(maxBoats))]

            # Place every remaining boat
            for i, amount in enumerate(remainingBoats):
                # TODO: Handle case if boat is not placed.
                # TODO: Handle coordinate to index conversion
                for z in range(amount):
                    print(f"Place boat with length {i}, {amount - z} remaining")
                    # Create boat
                    boat = class_boat(
                        length=i,
                        x=int(input("X: ")),
                        y=int(input("Y: ")),
                        isVertical=input("Vertical? (y/n): ").lower() == "y"
                    )
                    if not self.server == None:
                        player.getBoard().placeBoat(boat) # Check client first
                        self.server.sendPlaceBoat(boat)
                    else:
                        player.getBoard().placeBoat(boat)

    def setupAuto(self):
        """Automatically setup the game"""
        # NOTE: May get stuck with placing boats when placed inefficient
        for player in self.players:
            if self.server is not None and player is not self.server.getPlayer(): break # Prevent setup of other players if playing online
            # NOTE: This could be replaced by:
            # remainingBoats = player.getBoard.maxBoats
            # Since the board is empty and thus existing boats 0.
            # This would allow to place boats even if there are already boats residing on the board.
            board = player.getBoard()
            existingBoats = board.boats 
            maxBoats = board.maxBoats
            amountOfBoats = [len(amount) for amount in existingBoats] 
            remainingBoats = [maxBoats[i] - amountOfBoats[i] for i in range(len(maxBoats))]

            # Step through every remaining boat
            for i, amount in enumerate(reversed(remainingBoats)):
                length = len(remainingBoats) - i - 1 # Re- reverse the index
                for z in range(amount):
                    # While not all boats of length are placed, iterate the board and check for collision
                    y = 0
                    boat_placed = False
                    while y < board.size and not boat_placed:
                        x = 0 # Reset x
                        while x < board.size and not boat_placed:
                            boat = class_boat(
                                length=length,
                                x=x,
                                y=y,
                                isVertical=random.choice([True, False])
                            )
                            try:
                                if not self.server == None:
                                    player.getBoard().placeBoat(boat) # Check client first
                                    self.server.sendPlaceBoat(boat)
                                else:
                                    player.getBoard().placeBoat(boat)
                                    print(player.getBoard())
                                boat_placed = True
                            except ValueError:
                                x += 1
                        y += 1
    
    def play(self):
        """Play the game, not managed by server"""
        for player in self.players:
            while not all([boat.isDestroyed() for boat in player.getBoard().boats]):
                pass

    def playerTurn(self):
        """Handle a player turn"""
        for player in self.players:
            if self.server is not None and player is not self.server.getPlayer(): break # Prevent setup of other players if playing online
            print("Your turn!")
            print(player)
            print("Enter coordinates to shoot at")

            # Request coordinates until they are valid
            while True:
                x = input("X: ")
                y = input("Y: ")

                if x.isnumeric() and y.isnumeric():
                    x = int(x)
                    y = int(y)
                    x, y = class_board.toIndex(x, y)
                else:
                    print("Please enter a valid number (1-10)")
                    continue

                # Check if indexes are out of bounds or already shot at
                if x < 0 or y < 0 or x >= player.enemy.getBoard().size or y >= player.enemy.getBoard().size:
                    # (x or y) < 0 is handled by isnumeric() 
                    print("Coordinates out of bounds (1-10)")
                    continue
                elif player.enemy.getBoard().getState(x, y) != "?":
                    print("Coordinates already shot at")
                    continue
                break

            if not self.server == None:
                self.server.sendPlaceShot(x, y)
            else:
                player.enemy.getBoard().shoot(x, y)

    def getPlayer(self, name):
        """Return player object by name"""
        for player in self.players:
            if player.name == name:
                return player