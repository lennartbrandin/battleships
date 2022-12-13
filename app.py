from board import board
from boat import boat


class player:
    def __init__(self, board, name):
        self.board = board
        self.name = name

    def __str__(self):
        return f"{self.name}'s board: \n{self.board}"

    def getBoard(self):
        """Return board object"""
        return self.board

class game:
    def __init__(self, playerName1="Player1", playerName2="Player2"):
        """Create a local game consisting of two players, each with their own board"""
        self.p1 = player(board(),playerName1)
        self.p2 = player(board(),playerName2)
        self.players = [self.p1, self.p2]

    def __str__(self):
        return f"{self.p1.name}'s board: \n{self.p1.getBoard()} \n{self.p2.name}'s board: \n{self.p2.getBoard()}"

    def placeBoat(self, player, length, isVertical, x, y):
        """Get player inputs on the boat placement"""
        print(player.name + "'s turn to place boats")
        print("Enter the coordinates of the boat you want to place")
        placeOn = player.getBoard()

        def exists(*var):
            """Return var if it exists, else None"""
            return [i != None for i in var]

        # Only request user input if no arguments are passed
        if not all(exists(length, isVertical, x, y)):
            # length = int(input("Length: ")) # Length is given by placeBoats loop
        
            # Allow a default value for isVertical, convert to boolean and validate input
            isVertical = input("Vertical? (Y/n): ").lower()
            isVertical = True if isVertical == "y" or isVertical == '' else False if isVertical == "n" else None
            if isVertical == None:
                raise ValueError("Invalid input")

            x = int(input("x: "))
            y = int(input("y: "))

        boat(placeOn, length, isVertical, x, y)
        print(self.p1)

    def placeBoats(self, player, length=None, isVertical=None, x=None, y=None): # Optionally pass arguments
        """Place all boats on the board"""
        # Manual placement
        if all([i != None for i in [isVertical, x, y]]):
            # If arguments are passed, place a single boat
            self.placeBoat(player, length, isVertical=isVertical, x=x, y=y)
        else:
            # Place boat as long as the sum of existing boats is smaller than the sum of maximum boats
            existingBoats = player.getBoard().boats # List of list of boat objects differed by length of boat
            maxBoats = player.getBoard().maxBoats # List of maximum boats per length
            amountOfBoats = [len(amount) for amount in existingBoats] # List of boat amounts differed by length of boat
            remainingBoats = [maxBoats[i] - amountOfBoats[i] for i in range(len(maxBoats))]

            # Iterate through all boat types
            for length in range(len(remainingBoats)):
                # Place all boats of a certain length
                for amount in range(remainingBoats[length]):
                    if remainingBoats[length] > 0:
                        # Skip if all boats have been placed, or there is no boat of length 0, 1
                        print(f"Remaining boats of length: {length} to place: {remainingBoats[length]}")
                        self.placeBoat(player, length, isVertical, x, y) # Further pass optional arguments
                    remainingBoats[length] -= 1

    def predefinedBoats(self):
        for player in [self.p1]:
            for i in range(1, 5):
                self.placeBoats(player, 2, True, i*2, 1)
            for i in range(1, 4):
                self.placeBoats(player, 3, True, i*2, 4)
            for i in range(4, 6):
                self.placeBoats(player, 4, True, i*2, 4)
            self.placeBoats(player, 5, False, 1, 8)

if __name__=="__main__":
    game = game()

    # Hardcode boat placements
    game.predefinedBoats()
    print(game)

    # Place boats
    # for player in [game.p1]:#game.players:
    #     game.placeBoats(player)
    # print(game)

    # Shooting phase, loop until all boats are sunk
    activePlayer = game.players[0]
    activePlayerID = 0
    inactivePlayer = game.players[1]
    inactivePlayerID = 1
    # Flatten the isSunk status to a single list and check if all boats are not sunk
    while not all(sum(sum([[[boat.isSunk() for boat in boats] for boats in player.getBoard().boats] for player in game.players], []), [])):
        print(f"{activePlayer.name}'s turn to shoot")
        while inactivePlayer.getBoard().shoot(int(input("x: ")), int(input("y: "))):
            print(f"HIT, {activePlayer.name}'s turn to shoot")
        print(activePlayer.getBoard())
        # Switch active player
        activePlayer, inactivePlayer = inactivePlayer, activePlayer

    print(f"{inactivePlayer.name} won!")