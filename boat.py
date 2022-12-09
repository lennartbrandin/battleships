class boat:
    def __init__(self, board, length, isVertical, x, y):
        """Create a boat object and place it on the board"""
        self.length = length
        self.ID = length # Numeric representation in the board array
        self.isVertical = isVertical # True: array from top to bottom, False: array from left to right.
        self.isHit = [False for i in range(length)]
        self.xPos = x # Starting x position
        self.yPos = y # Starting y position

        board.placeBoat(self, x, y)

    def __str__(self):
        """return ID of boat"""
        return "X" if self.isSunk() else str(self.ID)


    def hit(self, x, y):
        """Hit a coordinate on the boat"""
        if self.isVertical:
            self.isHit[y - self.yPos] = True
        else:
            self.isHit[x - self.xPos] = True
        # Returns true is boat is sunk
        return self.isSunk()

    def isSunk(self):
        """Check if the boat is sunk"""
        # Return True if all components are hit
        return all(self.isHit)
 
    def getID(self):
        """Return the ID of the boat, it also represents the length of the boat"""
        return self.ID

    def getSize(self):
        """Return the length of the boat"""
        return self.length

    def getIntegrity(self):
        """Return the integrity of the boat"""
        return self.isHit