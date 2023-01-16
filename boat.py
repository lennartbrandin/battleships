class boat:
    def __init__(self, length, isVertical, x, y, isDestroyed=False):
        self.length=length
        self.isVertical=isVertical
        self.x=x
        self.y=y
        self.hits=[False if not isDestroyed else True for i in range(length)]

    def __str__(self):
        return f"{boat.length}"
        

    def getIndexes(self):
        """Get indexes of boat"""
        return self.x, self.y

    def getCollisionArea(self):
        """Get indexes of boat and surrounding indexes"""
        if self.isVertical:
            return [(self.x, self.y+i) for i in range(-1, self.length+1)]
        else:
            return [(self.x+i, self.y) for i in range(-1, self.length+1)]

    def hit(self, x, y):
        """Mark hits at index as hit"""
        boatX, boatY = self.getIndexes()
        if self.isVertical:
            self.hits[y-boatY] = True
        else:
            self.hits[x-boatX] = True
        return self.isSunk()

    def isHit(self, x, y):
        """Check if hits is hit at index"""
        boatX, boatY = self.getIndexes()
        if self.isVertical:
            return self.hits[y-boatY]
        else:
            return self.hits[x-boatX]

    def isSunk(self):
        """Check if boat is sunk"""
        return all(self.hits)