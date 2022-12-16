from board import board as class_board
from boat import boat as class_boat

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
                for i in range(amount):
                    print(f"Place boat with length {remainingBoats.index(amount)}, {amount} remaining")
                    # Create boat
                    boat = class_boat(
                        length=remainingBoats.index(amount),
                        x=input("X: "),
                        y=input("Y: "),
                        isVertical=input("Vertical? (y/n): ").lower == "y"
                    )
                    # Only place boat on board if server accepted it
                    # This will prefer server side checks over client side checks
                    if not self.server == None:
                        if self.server.sendPlaceBoat(boat):
                            player.getBoard().placeBoat(boat)
                    else:
                        player.getBoard().placeBoat(boat)