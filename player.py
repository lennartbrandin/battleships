class player:
    """A player in the game"""
    def __init__(self, game, name, filler):
        self.game=game
        self.name=name
        self.board=game.boardBlueprint(game, filler)

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

    
    def setEnemy(self, enemyName):
        """Set the enemy of the player"""
        self.enemy=enemy(self, enemyName)

    def shootSelf(self, x, y, override=False):
        """Shoot indexes at self, return if isHit"""
        return self.board.placeShot(x, y, override)

    def shootEnemy(self, x, y, override=False):
        """Shoot enemy at indexes, return if isHit"""
        # TODO: Add websocket communication
        return self.enemy.shootSelf(x, y, override)
                
class enemy(player):
    """An enemy of a player, holding all known information about the enemy"""
    def __init__(self, player, name):
        super().__init__(player.game, name, '?')

class ai(player):
    """An AI player"""
    def __init__(self, game, name):
        super().__init__(game, name, '0')

if __name__=="__main__":
    from game import game
    g = game(disableUI=True)
    p = ai(g, "Player")
    p.setEnemy("Enemy")
    p.shootEnemy(0, 0)
    print(p)