""" Define room types and movement actions """
import entities
import maps
import controls


class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def intro_text(self):
        raise NotImplementedError()

    def modify_player(self, player):
        raise NotImplementedError()

    def adjacent_moves(self):
        """Returns all move actions for adjacent tiles."""
        moves = []
        if maps.world.tile_exists(self.x + 1, self.y):
            moves.append(controls.actions.MoveEast())
        if maps.world.tile_exists(self.x - 1, self.y):
            moves.append(controls.actions.MoveWest())
        if maps.world.tile_exists(self.x, self.y - 1):
            moves.append(controls.actions.MoveNorth())
        if maps.world.tile_exists(self.x, self.y + 1):
            moves.append(controls.actions.MoveSouth())
        return moves

    def available_actions(self):
        """Returns all of the available actions in this room."""
        moves = self.adjacent_moves()
        moves.append(controls.actions.ViewInventory())

        return moves


class StartingRoom(MapTile):
    def intro_text(self):
        return """
        Welcome to the game!
        """

    def modify_player(self, player):
        # Room has no action on player
        pass


class LeaveCaveRoom(MapTile):
    def intro_text(self):
        return """
        You see a bright light in the distance...
        ... it grows as you get closer! It's sunlight!
 
 
        Victory is yours!
        """
 
    def modify_player(self, player):
        entities.player.Player().victory = True


class LootRoom(MapTile):
    def __init__(self, x, y, item):
        self.item = item
        super().__init__(x, y)

    def add_loot(self, player):
        entities.player.Player().inventory.append(self.item)

    def modify_player(self, player):
        self.add_loot(player)


class EnemyRoom(MapTile):
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x, y)

    def modify_player(self, the_player):
        if self.enemy.is_alive():
            the_player.hp = the_player.hp - self.enemy.damage
            print("Enemy does {} damage. You have {} HP remaining.\n".format(self.enemy.damage, the_player.hp))

    def available_actions(self):
        if self.enemy.is_alive():
            return [controls.actions.Flee(tile=self), controls.actions.Attack(enemy=self.enemy)]
        else:
            return self.adjacent_moves()


class EmptyCavePath(MapTile):
    def intro_text(self):
        return """
        Another unremarkable part of the cave. You must forge onwards.
        """

    def modify_player(self, player):
        # Room has no action on player
        pass


class SpiderRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, entities.enemies.Spider())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            \nA giant spider jumps down from its web in front of you!
            """
        else:
            return """
            The corpse of a dead spider rots on the ground.
            """


class OgreRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, entities.enemies.Ogre())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
           \n A giant orge blocks your path!
            """
        else:
            return """
            A dead ogre is stinking the place up. Someone should move that.
            """


class DaggerRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, entities.items.Dagger())

    def intro_text(self):
        return """
        \nYour notice something shiny in the corner.
        It's a dagger! You pick it up.
        """


class GoldRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, entities.items.Gold())

    def intro_text(self):
        return """
        \nYou've found a pile of coins!
        I have no idea who left them there, but hey look fair game to me!
        """
