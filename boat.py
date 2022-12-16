class boat:
    def __init__(self, length, isVertical, x, y):
        """Create a boat object and place it on the board"""
        self.length = length
        self.ID = length # Numeric representation in the board array
        self.isVertical = isVertical # True: array from top to bottom, False: array from left to right.
        self.isHit = [False for i in range(length)]
        self.xPos = x # Starting x position
        self.yPos = y # Starting y position

    def __str__(self):
        """return ID of boat"""
        return "S" if self.isSunk() else str(self.ID)


    def hit(self, x, y):
        """Hit a coordinate on the boat"""
        boatX, boatY = self.xPos-1, self.yPos-1 # Convert coordinates to array indexes
        if self.isVertical:
            self.isHit[y - boatY] = True
        else:
            self.isHit[x - boatX] = True
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

    def getCoordinates(self):
        """Return the coordinates of the boat"""
        return [self.xPos, self.yPos]