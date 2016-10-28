import sys
import random
import configparser
import entities.enemies as enemies

class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = ''

    def intro_text(self):
        raise NotImplementedError("Create a subclass instead!")

    def modify_player(self, player):
        pass


class StartTile(MapTile):
    def intro_text(self):
        return """
        You find yourself in a cave with a flickering torch on the wall.
        You can make out four paths, each equally as dark and foreboding.
        """


class BoringTile(MapTile):
    def intro_text(self):
        return """
        This is a very boring part of the cave. Fuck all happens here
        """


class VictoryTile(MapTile):
    def intro_text(self):
        return """
        You see a bright light in the distance...
        ... it grows as you get closer! It's sunlight!


        Victory is yours!
        """


class EnemyTile(MapTile):
    def __init__(self, x, y):
        encounter_type = random.random()

        if encounter_type < 0.50:
            self.enemy = enemies.GiantSpider()
            self.alive_text = "A giant spider jumps down from " \
                              "its web and lands right in front " \
                              "of you!"
            self.dead_text = "The lifeless corpse of the spider " \
                             "slumps in the corner. Creepy."
        elif encounter_type < 0.80:
            self.enemy = enemies.Ogre()
            self.alive_text = "A ogre blocks your path!"
            self.dead_text = "The orge dies convinietly off of " \
                             "the path, out of the way."
        elif encounter_type < 0.95:
            self.enemy = enemies.BatColony()
            self.alive_text = "Rats. Eeshk..."
            self.dead_text = "The furry bastards are dead"
        else:
            self.enemy = enemies.RockMonster()
            self.alive_text = "Is it a bird? Is it a plane? no " \
                              "it's a rock monster!"
            self.dead_text = "You killed a rock. " \
                             "Now thats dedication!!"

        super().__init__(x, y)

    def intro_text(self):
        if self.enemy.is_alive():
            return self.alive_text
        else:
            return self.dead_text

    def modify_player(self, player):
        if self.enemy.is_alive():
            player.hp = player.hp - self.enemy.damage
            print("Enemy does {} damage. You have {} HP remaining."
                  .format(self.enemy.damage, player.hp))

world_map = []

start_tile_location = None

tile_type_dict = {"VT": VictoryTile,
                  "EN": EnemyTile,
                  "ST": StartTile,
                  "  ": None}


def is_dsl_valid(dsl):
    if dsl.count("|ST|") != 1:
        return False

    if dsl.count("|VT|") == 0:
        return False

    lines = dsl.splitlines()
    lines = [l for l in lines if l]
    pipe_counts = [line.count("|") for line in lines]

    for count in pipe_counts:
        if count != pipe_counts[0]:
            return False

    return True

def parse_world_dsl(map_file):
    level_map = open(map_file, 'r').read()

    if not is_dsl_valid(level_map):
        sys.exit("Rumtime error: unable to parse map file")

    dsl_lines = level_map.splitlines()
    dsl_lines = [x for x in dsl_lines if x]

    for y, dsl_row in enumerate(dsl_lines):
        row = []
        dsl_cells = dsl_row.split("|")
        dsl_cells = [c for c in dsl_cells if c]

        for x, dsl_cell in enumerate(dsl_cells):
            if dsl_cell not in tile_type_dict:
                sys.exit("Map parse error: Invalid room type in map")
                break

            tile_type = tile_type_dict[dsl_cell]
            if tile_type == StartTile:
                global start_tile_location
                start_tile_location = x, y
            row.append(tile_type(x, y) if tile_type else None)

        world_map.append(row)

def tile_at(x, y):
    if x < 0 or y < 0:
        return None

    try:
        return world_map[y][x]
    except IndexError:
        return None
