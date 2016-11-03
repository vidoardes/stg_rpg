"""Define availible tiles and their actions, and build level from map file"""

import sys
import random
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
        print("                         `-._\\/  .  \\ /    |/_")
        print("                             \\  _\\, y | \\//")
        print("                       _\\_.___\\, \\/ -.\\||")
        print("                         `7-,--.`._||  / / ,")
        print("                         /'     `-. `./ / |/_.'")
        print("                                   |    |//")
        print("                                   |_    /")
        print("                                   |-   |")
        print("                                   |   =|")
        print("                                   |    |")
        print("              --------------------/ ,  . \\--------._")
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

        if encounter_type < 0.30:
            self.enemy = enemies.GiantSpider()
            self.alive_text = "\nA giant spider jumps down from " \
                              "its web and lands right in front " \
                              "of you!"
            self.dead_text = "\nThe lifeless corpse of the spider " \
                             "slumps in the corner. Creepy."
        elif encounter_type < 0.60:
            self.enemy = enemies.Goblin()
            self.alive_text = "\nA nasty lttile goblin leaps out at you" \
                              "and waves his stabby daggar at you!"
            self.dead_text = "\nThe gblin exploded all over the walls." \
                             "I'm not cleaning that up.'"
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
        self.enemy.loot = self.enemy.randomise_stats(self.enemy.loot)

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
            print("{} has {} HP".format(self.enemy.name, self.enemy.hp))
        else:
            print("  ____   ____.___ _________  ___________________   __________ _____.___.._.")
            print("  \\   \\ /   /|   |\\_   ___ \\ \\__    ___/\\_____  \\  \\______   \\\\__  |   || |")
            print("   \\   Y   / |   |/    \\  \\/   |    |    /   |   \\  |       _/ /   |   || |")
            print("    \\     /  |   |\\     \\____  |    |   /    |    \\ |    |   \\ \\____   | \\|")
            print("     \\___/   |___| \\______  /  |____|   \\_______  / |____|_  / / ______| __")
            print("                          \\/                    \\/         \\/  \\/        \\/")
            print(self.dead_text)

    def modify_player(self, player):
        if self.enemy.is_alive():
            dex_mod = decimal.Decimal(player.dex_stat / 100)
            dodge_chance = decimal.Decimal(random.random()) * dex_mod
            miss_chance = decimal.Decimal(random.random()) * dex_mod

            if miss_chance > 0.98:
                print("The {} missed!".format(self.enemy.name))
            elif dodge_chance > 0.98:
                print("You dodged the attack!")
            else:
                def_mod = decimal.Decimal(2 - (player.def_stat / 100))
                enemy_damage = round(self.enemy.damage * def_mod, 0)
                player.curr_hp -= enemy_damage
                print("The {} does {} damage. You have {} HP remaining."
                      .format(self.enemy.name, enemy_damage, player.curr_hp))


class TraderTile(MapTile):
    def __init__(self, x, y):
        self.trader = npc.Trader()
        super().__init__(x, y)

    def trade(self, buyer, seller):
        if len(seller.inventory) == 0:
            return

        for i, item in enumerate(seller.inventory, 1):
            print("{}. {} - {} Gold".format(i, item.name, item.value))

        while True:
            if len(seller.inventory) == 0:
                return

            user_input = input("\nChoose an item or press Q to exit: ")

            if user_input in ['Q', 'q']:
                return
            else:
                try:
                    choice = int(user_input)
                    if choice > len(seller.inventory) or choice < 1:
                        print("Invalid choice!")
                    else:
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
            if len(self.trader.inventory) == 0:
                print("No items to trade!")
                return

            user_input = input("Would you like to (B)uy, (S)ell, or (Q)uit?: ")

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
            luc_mod = decimal.Decimal(player.luc_stat / 100)
            found_loot = round(self.gold * luc_mod, 0) 
            player.gold += found_loot
            print("\n                You found {} gold coins!".format(found_loot))

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
    world_map = []
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
            tile = None

            if tile_type is not None:
                tile = tile_type(x, y)

            if tile_type == StartTile:
                global start_tile_location
                start_tile_location = x, y

            row.append(tile)

        world_map.append(row)

    return world_map
