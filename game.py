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
        return f"{self.name}:\n{self.board}"

    def getBoard(self):
        """Return the board of the player"""
        return self.board

class game:
    def __init__(self, server, *players):
        self.server = server
        self.players = players if server == None else [server.getPlayer()] # If playing online, copy the player names from the server
        self.activePlayerID = 0
    
    def __str__(self):
        return "\n".join([str(player) for player in self.players])

    def setup(self):
        """Setup the game"""
        # Place boat as long as the sum of existing boats is smaller than the sum of maximum boats
        for player in self.players:
            existingBoats = player.getBoard().boats # List of list of boat objects differed by length of boat
            maxBoats = player.getBoard().maxBoats # List of maximum boats per length
            amountOfBoats = [len(amount) for amount in existingBoats] # List of boat amounts differed by length of boat
            remainingBoats = [maxBoats[i] - amountOfBoats[i] for i in range(len(maxBoats))]


            # Place every remaining boat
            for amount in remainingBoats:
                # TODO: Handle case if boat is not placed.
                for i in range(amount):
                    print(f"Place boat with length {remainingBoats.index(amount)}, {amount - i} remaining")
                    # Create boat
                    boat = class_boat(
                        length=remainingBoats.index(amount),
                        x=int(input("X: ")),
                        y=int(input("Y: ")),
                        isVertical=input("Vertical? (y/n): ").lower == "y"
                    )
                    if not self.server == None:
                        player.getBoard().placeBoat(boat) # Check client first
                        self.server.sendPlaceBoat(boat)
                        print(player.getBoard()) # Only one player for online game
                    else:
                        player.getBoard().placeBoat(boat)
                        print(player.getBoard())

    def setupAuto(self):
        """Automatically setup the game"""
        # NOTE: May get stuck with placing boats when placed inefficient
        for player in self.players:
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
            for amount in reversed(remainingBoats):
                for i in range(amount):
                    # While not all boats of length are placed, iterate the board and check for collision
                    y = 0
                    boat_placed = False
                    while y < board.size and not boat_placed:
                        x = 0 # Reset x
                        while x < board.size and not boat_placed:
                            xPos, yPos = class_board.toCoordinates(x, y) # Convert index to coordinates
                            boat = class_boat(
                                length=remainingBoats.index(amount),
                                x=xPos,
                                y=yPos,
                                isVertical=random.choice([True, False])
                            )
                            try:
                                if not self.server == None:
                                    player.getBoard().placeBoat(boat) # Check client first
                                    self.server.sendPlaceBoat(boat)
                                    print(player.getBoard()) 
                                else:
                                    player.getBoard().placeBoat(boat)
                                    print(player.getBoard())
                                boat_placed = True
                            except ValueError:
                                x += 1
                        y += 1
