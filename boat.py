class boat:
    def __init__(self, board, length, isVertical, x, y):
        """Create a boat object and place it on the board"""
        self.length = length
        self.ID = length # Numeric representation in the board array
        self.isVertical = isVertical # True: array from top to bottom, False: array from left to right.
        self.xPos = x # Starting x position
        self.yPos = y # Starting y position
        self.integrity = [True for i in range(length)]

        board.placeBoat(self, isVertical, x, y)
 
    def getID(self):
        """Return the ID of the boat, it also represents the length of the boat"""
        return self.ID

    def getSize(self):
        """Return the length of the boat"""
        return self.length