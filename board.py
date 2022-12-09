class board:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self._board = [[0 for a in range(width)] for b in range(height)] # 2D array to represent the board, fill with 0s

    def __str__(self):
        """Return a formatted string of the board"""
        formattedString = ""
        for i in range(self.height):
            for j in range(self.width):
                formattedString += str(self._board[i][j]) + " "
            formattedString += "\n"
        return formattedString


    def placeBoat(self, boat, isVertical, x, y):
        """Place a boat on the board"""
        # TODO: Check if server has initialized the boat
        # if self.checkOutOfBounds(x, y) or self.checkOutOfBounds(x+boat.getSize(), y+boat.getSize()):
        #     raise ValueError("Coordinates are out of bounds")
        
        if self.getState(x, y) > 0:
            # -1 is miss, 0 is empty, 1 or larger is a type of boat
            raise ValueError("There is already a boat in this position")

        # Convert coordinates to array indexes
        x -= 1
        y -= 1

        if isVertical:
            # Fill array with boat ID horizontally or vertically
            for i in range(boat.getSize()):
                self._board[y+i][x] = boat.getID()
        else:
            for i in range(boat.getSize()):
                self._board[y][x+i] = boat.getID()

    # def checkOutOfBounds(self, x, y):
    #     """Check if coordinates are out of bounds"""
    #     if x < 0 or y < 0 or x > self.width or y > self.height:
    #         return True
    #     return False

    def getState(self, x, y):
        """Return the state of coordinates in the board"""
        return self._board[y][x]

    def getState(self, x, y):
        """Return a list of states of x-coordinates in the board"""
        return [self._board[y][i] for i in x]

    def getState(self, x, y):
        """Return a list of states of y-coordinates in the board"""
        return [self._board[i][x] for i in y]