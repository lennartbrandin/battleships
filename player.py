from ui.grid import grid as class_grid
class player:
    """A player in the game"""
    def __init__(self, game, name, filler):
        self.game=game
        self.name=name
        self.board=game.boardBlueprint(game, filler)
        self.isEnemy=False

    def __str__(self):
        """Return player, enemy and their boards as formatted string"""
        formattedString = f"{self.name}'s board:" 
        # Add spaces to align player/enemy names, and add 2 spaces to account for | and its space
        formattedString += " " * (2*self.game.size - len(formattedString) + 2) + f"{self.enemy.name}'s board:\n"
        for y in range(self.game.size):
            for x in range(self.game.size):
                formattedString += f"{self.board.get(x, y)} "
            formattedString += "| "
            for x in range(self.game.size):
                formattedString += f"{self.enemy.board.get(x, y)} "
            formattedString += "\n"
        return formattedString
    
    def setPhase(self, phase):
        """Set the current phase"""
        if phase == "WAITING_FOR_PLAYER":
            pass
        elif phase == "SETUP":
            self.grid = class_grid(self)
            self.grid.exec()
        elif phase == "IN_PROGRESS":
            pass
    
    def shipPlaced(self, x, y, length, isVertical):
        self.board.placeBoat(x, y, length, isVertical)
        self.grid.player.board.update()

    def shotFired(self, x, y, player, result):
        if self.enemy.name == player:
            self.board.placeShot(x, y)
            self.grid.player.board.update()
        else:
            self.enemy.board.placeShot(x, y, override=result)
            self.grid.enemy.board.update()

    def setEnemy(self, enemyName):
        """Set the enemy of the player"""
        self.enemy=enemy(self.game, enemyName)

    def shootSelf(self, x, y, override=False):
        """Shoot indexes at self, return if isHit"""
        return self.board.placeShot(x, y, override)

    def shootEnemy(self, x, y, override=False):
        """Shoot enemy at indexes, return if isHit"""
        # TODO: Add websocket communication
        return self.enemy.shootSelf(x, y, override)
                
class enemy(player):
    """An enemy of a player, holding all known information about the enemy"""
    def __init__(self, game, name):
        super().__init__(game, name, '?')
        self.isEnemy=True

class ai(player):
    """An AI player"""
    def __init__(self, game, name):
        super().__init__(game, name, '0')

if __name__=="__main__":
    from game import game
    g = game(disableUI=True)
    p = player(g, "Player", "0")
    p.setEnemy("Enemy")
    p.shootEnemy(0, 0)
    p.shootSelf(0, 0)
    print(p)