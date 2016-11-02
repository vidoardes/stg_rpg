"""Save the Girl!"""

import os
import pickle
import re
from collections import OrderedDict

import maps.world as world
from entities.player import Player


class GameInit:
    def __init__(self):
        self.map = world.parse_world_dsl("assets/level1.map")
        self.player = Player()


class GameManager:
    def __init__(self):
        self.map = None
        self.player = None
        pass

    def tile_at(self, x, y):
        if x < 0 or y < 0:
            return None

        try:
            return self.map[y][x]
        except IndexError:
            return None

    def start_game(self, player, world_map, load_save=False):
        clear()
        self.map = world_map
        self.player = player

        while self.player.is_alive() and not self.player.victory:
            room = self.tile_at(self.player.x, self.player.y)
            self.player.room = room

            if room.visited == 0 or load_save is True:
                load_save = False
                clear()
                room.intro_text()
                room.visited = 1

            room.modify_player(self.player)

            if self.player.is_alive() and not self.player.victory:
                self.choose_action(room, self.player)
            elif not self.player.is_alive():
                clear()
                print("You have been slain. \"The Villian\" has got \"The Girl\" :(")
                input("Press Enter to continue...")
                main_menu()

    def get_available_actions(self, room, player, list_available_actions):
        actions = OrderedDict()

        if self.player.inventory:
            self.action_adder(actions, 'i', self.player.print_inventory)
            list_available_actions['i'] = 'Show (I)nventory'

        if isinstance(room, world.TraderTile):
            self.action_adder(actions, 't', self.player.trade)
            list_available_actions['t'] = '(T)rade'

        if player.hp < 100:
            self.action_adder(actions, 'h', self.player.heal)
            list_available_actions['h'] = '(H)eal up'

        if isinstance(room, world.EnemyTile) and room.enemy.is_alive():
            self.action_adder(actions, 'a', self.player.attack)
            list_available_actions['a'] = '(A)ttack!'
        else:
            if self.tile_at(room.x, room.y - 1):
                self.action_adder(actions, 'n', self.player.move_north)
                list_available_actions['n'] = 'Go (N)orth'
            if self.tile_at(room.x, room.y + 1):
                self.action_adder(actions, 's', self.player.move_south)
                list_available_actions['s'] = 'Go (S)outh'
            if self.tile_at(room.x + 1, room.y):
                self.action_adder(actions, 'e', self.player.move_east)
                list_available_actions['e'] = 'Go (E)ast'
            if self.tile_at(room.x - 1, room.y):
                self.action_adder(actions, 'w', self.player.move_west)
                list_available_actions['w'] = 'Go (W)est'

        self.action_adder(actions, 'p', self.save_game)
        list_available_actions['p'] = 'Save (P)rogress'

        self.action_adder(actions, 'x', main_menu)
        list_available_actions['x'] = 'E(x)it to Main Menu'

        return actions

    def action_adder(self, action_dict, hotkey, action):
        action_dict[hotkey.lower()] = action
        action_dict[hotkey.upper()] = action

    def choose_action(self, room, player):
        action = None
        list_available_actions = OrderedDict()

        while not action:
            available_actions = self.get_available_actions(room, self.player, list_available_actions)
            action_input = input("\nChoose an action (type '?'' for help):")
            action = available_actions.get(action_input)

            if action_input == '?':
                print("")
                for key, name in list_available_actions.items():
                    print(key + ': ' + name)
            elif action:
                action()
            else:
                print("You can't do that here")

    def save_game(self):
        data = {"map": self.map,
                "player": self.player}
        if not os.path.exists('saves'):
            os.makedirs('saves')

        clear()
        save_name = input("Please enter a filename for the save: ")

        save_name = re.sub(r'\W+', '', save_name)

        pickle.dump(data, open("saves/" + save_name + ".dat", "wb"))
        clear()
        print("Your progress has been saved!")
        input("Press enter to continue...")
        main_menu()


def clear():
    return os.system('cls')


def main_menu():
    menu_choice = None

    clear()
    print("  __________________________________________________________________________________________ ")
    print(" |  _______                           _______  __                _______  __        __  __  |")
    print(" | |     __|.---.-..--.--..-----.    |_     _||  |--..-----.    |     __||__|.----.|  ||  | |")
    print(" | |__     ||  _  ||  |  ||  -__|      |   |  |     ||  -__|    |    |  ||  ||   _||  ||__| |")
    print(" | |_______||___._| \___/ |_____|      |___|  |__|__||_____|    |_______||__||__|  |__||__| |")
    print(" |__________________________________________________________________________________________|")

    print("\n   You are \"The Guy\" and everything was great, until \"The Villan\" came along and took your")
    print("    girl! Run through dungeons and battle creatures to rescue \"The Girl\" and save the day!")
    print("\n              1. Start New Game")
    print("              2. Load Saved Game")
    print("              3. Exit")

    while True:
        menu_choice = input('\n>>> ')

        if menu_choice == '2':
            load_game()
        elif menu_choice == '3':
            clear()
            quit_game = input("Are you sure you want to quit? (Y/N): ")

            if quit_game == 'n':
                main_menu()
            elif quit_game == 'y':
                print("Thanks for playing!")
                exit()
            else:
                main_menu()
        elif menu_choice == '1':
            new_game = GameInit()
            start_game = GameManager()
            start_game.start_game(new_game.player, new_game.map)
        else:
            main_menu()


def load_game():
    list_saves = OrderedDict()
    save_choice = None

    if not os.path.exists('saves'):
        os.makedirs('saves')

    for idx, save_file in enumerate(os.listdir("saves")):
        if save_file.endswith(".dat"):
            list_saves[str(idx+1)] = save_file

    if len(list_saves) > 0:
        clear()
        print(list_saves)
        print("Your Saved Games")
        print("----------------\n")

        for key, val in list_saves.items():
            print("    " + str(key) + ": " + val)

        print("    q: Back to main menu")

        while save_choice not in list_saves:
            save_choice = input("\nPlease select which file you wish to load: ")

            if save_choice == 'q':
                main_menu()
            elif save_choice in list_saves:
                load_save = pickle.load(open("saves/" + list_saves[save_choice], "rb"))
                load_player = load_save["player"]
                load_map = load_save["map"]
                load_game = GameManager()
                load_game.start_game(load_player, load_map, True)
            else:
                print("Invalid Choice")
    else:
        clear()
        print("No save file found!")
        input("Press enter to continue...")
        main_menu()


if __name__ == '__main__':
    main_menu()