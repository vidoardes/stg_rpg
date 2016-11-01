"""Save the Girl!"""

import os
from collections import OrderedDict

import maps.world as world
from entities.player import Player

class GameManager:
    def __init__(self):
        self.map = ''

    def tile_at(self, x, y):
        if x < 0 or y < 0:
            return None

        try:
            return self.map[y][x]
        except IndexError:
            return None

    def start_new_game(self):
        clear()
        self.map = world.parse_world_dsl("maps/level1.map")
        player = Player()

        while player.is_alive() and not player.victory:
            room = self.tile_at(player.x, player.y)
            player.room = room

            if room.visited == 0:
                clear()
                room.intro_text()
                room.visited = 1

            room.modify_player(player)

            if player.is_alive() and not player.victory:
                self.choose_action(room, player)
            elif not player.is_alive():
                clear()
                print("You have been slain. \"The Villian\" has got \"The Girl\" :(")
                input("Press Enter to continue...")
                main_menu()


    def get_available_actions(self, room, player, list_available_actions):
        actions = OrderedDict()

        if player.inventory:
            self.action_adder(actions, 'i', player.print_inventory)
            list_available_actions['i'] = 'Show Inventory'

        if isinstance(room, world.TraderTile):
            self.action_adder(actions, 't', player.trade)
            list_available_actions['t'] = 'Trade'

        if player.hp < 100:
            self.action_adder(actions, 'h', player.heal)
            list_available_actions['h'] = 'Heal up'

        if isinstance(room, world.EnemyTile) and room.enemy.is_alive():
            self.action_adder(actions, 'a', player.attack)
            list_available_actions['a'] = 'Attack!'
        else:
            if self.tile_at(room.x, room.y - 1):
                self.action_adder(actions, 'n', player.move_north)
                list_available_actions['n'] = 'Go north'
            if self.tile_at(room.x, room.y + 1):
                self.action_adder(actions, 's', player.move_south)
                list_available_actions['s'] = 'Go south'
            if self.tile_at(room.x + 1, room.y):
                self.action_adder(actions, 'e', player.move_east)
                list_available_actions['e'] = 'Go east'
            if self.tile_at(room.x - 1, room.y):
                self.action_adder(actions, 'w', player.move_west)
                list_available_actions['w'] = 'Go west'

        self.action_adder(actions, 'q', quit_game)
        list_available_actions['q'] = 'Quit'

        self.action_adder(actions, 'p', save_game)
        list_available_actions['p'] = 'Save'

        return actions


    def action_adder(self, action_dict, hotkey, action):
        action_dict[hotkey.lower()] = action
        action_dict[hotkey.upper()] = action


    def choose_action(self, room, player):
        action = None
        list_available_actions = OrderedDict()

        while not action:
            available_actions = self.get_available_actions(room, player, list_available_actions)
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
    print("              2. Exit")

    while True:
        menu_choice = input('\n>>> ')

        if menu_choice == '3':
            load_game()
        elif menu_choice == '2':
            quit_game()
        elif menu_choice == '1':
            new_game = GameManager()
            new_game.start_new_game()
        else:
            main_menu()


def save_game():
    return

def load_game():
    return

def quit_game():
    clear()
    print("Thanks for playing!")
    exit()

if __name__ == '__main__':
    main_menu()
