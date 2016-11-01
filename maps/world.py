import sys
import random
import configparser
import decimal

import entities.enemies as enemies
import entities.npc as npc


class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = 0
        self.type = ''

    def intro_text(self):
        raise NotImplementedError("Create a subclass instead!")

    def modify_player(self, player):
        pass


class StartTile(MapTile):
    def intro_text(self):
        print("\n         ^  ^  ^   ^      ___I_      ^  ^   ^  ^  ^   ^  ^")
        print("        /|\\/|\\/|\\ /|\\    /\\-_--\\    /|\\/|\\ /|\\/|\\/|\\ /|\\/|\\")
        print("        /|\\/|\\/|\\ /|\\   /  \\_-__\\   /|\\/|\\ /|\\/|\\/|\\ /|\\/|\\")
        print("        /|\\/|\\/|\\ /|\\   |[]| [] |   /|\\/|\\ /|\\/|\\/|\\ /|\\/|\\")
        print("\n                     LEVEL 1: The Forest")
        print("\n       You chase \"The Villain\" to the edge of a forest.")
        print("    Looks like you are going to have to head in after him....")


class BoringTile(MapTile):
    def intro_text(self):
        print("\n                            v .   ._, |_  .,")
        print("                         `-._\/  .  \ /    |/_")
        print("                             \\  _\, y | \//")
        print("                       _\_.___\\, \\/ -.\||")
        print("                         `7-,--.`._||  / / ,")
        print("                         /'     `-. `./ / |/_.'")
        print("                                   |    |//")
        print("                                   |_    /")
        print("                                   |-   |")
        print("                                   |   =|")
        print("                                   |    |")
        print("              --------------------/ ,  . \--------._")
        print("\n This is a very boring part of the forest. Fuck all happens here")


class VictoryTile(MapTile):
    def modify_player(self, player):
        player.victory = True
        exit()

    def intro_text(self):
        print("\n                                            .''.")
        print("          .''.             *''*    :_\/_:     .")
        print("         :_\/_:   .    .:.*_\/_*   : /\ :  .'.:.'.")
        print("     .''.: /\ : _\(/_  ':'* /\ *  : '..'.  -=:o:=-")
        print("    :_\/_:'.:::. /)\*''*  .|.* '.\'/.'_\(/_'.':'.'")
        print("    : /\ : :::::  '*_\/_* | |  -= o =- /)\    '  *")
        print("     '..'  ':::'   * /\ * |'|  .'/.\'.  '._____")
        print("         *        __*..* |  |     :      |.   |' .---\"|")
        print("          _*   .-'   '-. |  |     .--'|  ||   | _|    |")
        print("       .-'|  _.|  |    ||   '-__  |   |  |    ||      |")
        print("       |' | |.    |    ||       | |   |  |    ||      |")
        print("   ____|  '-'     '    ""       '-'   '-.'    '`      |____")
        print("   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ")
        print("\n                      You Saved \"The Girl\"!")
        print("\n You whisk her unto your arms and dissaper in to the sunset!")
        print("          Lets hope she makes it worth your while ;)")
        print("\n\n                  Thanks for playing the game!")


class EnemyTile(MapTile):
    def __init__(self, x, y):
        encounter_type = random.random()

        if encounter_type < 0.50:
            self.enemy = enemies.GiantSpider()
            self.alive_text = "\nA giant spider jumps down from " \
                              "its web and lands right in front " \
                              "of you!"
            self.dead_text = "\nThe lifeless corpse of the spider " \
                             "slumps in the corner. Creepy."
        elif encounter_type < 0.80:
            self.enemy = enemies.Ogre()
            self.alive_text = "\nA ogre blocks your path!"
            self.dead_text = "\nThe oger died convinietly off of " \
                             "the path, out of the way."
        elif encounter_type < 0.95:
            self.enemy = enemies.BatColony()
            self.alive_text = "\nBats. Eeshk..."
            self.dead_text = "\nThe furry bastards are dead"
        else:
            self.enemy = enemies.RockMonster()
            self.alive_text = "\nIs it a bird? Is it a plane? no " \
                              "it's a rock monster!"
            self.dead_text = "\nYou killed a rock. " \
                             "Now thats dedication!!"

        self.enemy.hp = self.enemy.randomise_stats(self.enemy.hp)
        self.enemy.damage = self.enemy.randomise_stats(self.enemy.damage)

        super().__init__(x, y)

    def intro_text(self):
        if self.enemy.is_alive():
            print("\n  ___________.___   ________   ___ ___  ___________._.")
            print("  \\_   _____/|   | /  _____/  /   |   \\ \\__    ___/| |")
            print("   |    __)  |   |/   \\  ___ /    ~    \\  |    |   | |")
            print("   |     \\   |   |\\    \\_\\  \\\\    Y    /  |    |    \\|")
            print("   \\___  /   |___| \\______  / \\___|_  /   |____|    __")
            print("       \\/                 \\/        \\/              \\/")
            print(self.alive_text)
            print(self.enemy.name + " has " + str(self.enemy.hp) + " HP")
        else:
            print("  ____   ____.___ _________  ___________________   __________ _____.___.._.")
            print("  \\   \ /   /|   |\\_   ___ \\ \\__    ___/\\_____  \\  \\______   \\\\__  |   || |")
            print("   \\   Y   / |   |/    \\  \\/   |    |    /   |   \\  |       _/ /   |   || |")
            print("    \\     /  |   |\\     \\____  |    |   /    |    \\ |    |   \\ \\____   | \\|")
            print("     \\___/   |___| \\______  /  |____|   \\_______  / |____|_  / / ______| __")
            print("                          \\/                    \\/         \\/  \\/        \\/")
            print(self.dead_text)

    def modify_player(self, player):
        if self.enemy.is_alive():
            player.hp = player.hp - round(round(decimal.Decimal(random.uniform(0.85, 1.15)), 2) * self.enemy.damage, 0)
            print("Enemy does {} damage. You have {} HP remaining."
                  .format(self.enemy.damage, player.hp))


class TraderTile(MapTile):
    def __init__(self, x, y):
        self.trader = npc.Trader()
        super().__init__(x, y)

    def trade(self, buyer, seller):
        for i, item in enumerate(seller.inventory, 1):
            print("{}. {} - {} Gold".format(i, item.name, item.value))

        while True:
            user_input = input("\nChoose an item or press Q to exit: ")

            if user_input in ['Q', 'q']:
                return
            else:
                try:
                    choice = int(user_input)
                    to_swap = seller.inventory[choice - 1]
                    self.swap(seller, buyer, to_swap)
                except ValueError:
                    print("Invalid choice!")

    def swap(self, seller, buyer, item):
        if item.value > buyer.gold:
            print("That's too expensive")
            return

        seller.inventory.remove(item)
        buyer.inventory.append(item)
        seller.gold = seller.gold + item.value
        buyer.gold = buyer.gold - item.value
        print("Trade complete!")

    def check_if_trade(self, player):
        while True:
            print("Would you like to (B)uy, (S)ell, or (Q)uit?")
            user_input = input()

            if user_input in ['Q', 'q']:
                return
            elif user_input in ['B', 'b']:
                print("Here's whats available to buy:\n")
                self.trade(buyer=player, seller=self.trader)
            elif user_input in ['S', 's']:
                print("Here's whats available to sell:\n")
                self.trade(buyer=self.trader, seller=player)
            else:
                print("Invalid choice!")

    def intro_text(self):
        print("\n                      _________##")
        print("                     @\\\\\\\\\\\\\\\\\\##")
        print("                    @@@\\\\\\\\\\\\\\\\##\\")
        print("                   @@ @@\\\\\\\\\\\\\\\\\\\\\\")
        print("                  @@@@@@@\\\\\\\\\\\\\\\\\\\\\\")
        print("                 @@@@@@@@@----------|")
        print("                 @@ @@@ @@__________|")
        print("                 @@@@@@@@@__________|")
        print("                 @@@@ .@@@__________|")
        print("           _\|/__@@@@__@@@__________|__")
        print("\n                   Trading Post")
        print("\n               Press \"T\" to trade")


class FindGoldTile(MapTile):
    def __init__(self, x, y):
        self.gold = random.randint(20, 75)
        self.gold_claimed = False
        super().__init__(x, y)

    def modify_player(self, player):
        if not self.gold_claimed:
            self.gold_claimed = True
            player.gold = player.gold + self.gold
            print("\n                You found {} gold coins!".format(self.gold))

    def intro_text(self):
        print("\n           |#######=====================#######|")
        print("           |#(1)*UNITED STATES OF WHAYEVER*(1)#|")
        print("           |#**           /===\   ********  **#|")
        print("           |*# {G}       | (\") |             #*|")
        print("           |#*  ******   | /v\ |    O N E    *#|")
        print("           |#(1)          \===/            (1)#|")
        print("           |##===========SOME GOLD===========##|")
        if self.gold_claimed:
            print("\n            You've already looted this place!")
        else:
            print("\n         Someone dropped some gold. You pick it up.")


world_map = []

start_tile_location = None

tile_type_dict = {"VT": VictoryTile,
                  "EN": EnemyTile,
                  "ST": StartTile,
                  "NA": BoringTile,
                  "FG": FindGoldTile,
                  "TT": TraderTile,
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
