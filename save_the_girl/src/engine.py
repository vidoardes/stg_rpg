import os
import pickle
import re
from collections import OrderedDict

import src.world as world
from src.player import Player


class GameInit:
    def __init__(self):
        self.map = world.parse_world_dsl("assets/level1.map")
        self.player = Player()


class GameManager:
    main_menu = False

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
        global main_menu
        main_menu = False
        os.system('cls')
        self.map = world_map
        self.player = player

        while self.player.is_alive() and not self.player.victory and main_menu == False:
            room = self.tile_at(self.player.x, self.player.y)
            self.player.room = room

            if room.visited == 0 or load_save is True:
                load_save = False
                os.system('cls')
                room.intro_text()
                room.visited = 1

            room.modify_player(self.player)

            if self.player.is_alive() and not self.player.victory:
                self.choose_action(room, self.player)
            elif not self.player.is_alive():
                os.system('cls')
                print("You have been slain. \"The Villian\" has got \"The Girl\" :(")
                input("Press Enter to continue...")
                pass

    def get_available_actions(self, room, player, list_available_actions):
        actions = OrderedDict()

        if isinstance(room, world.TraderTile):
            self.action_adder(actions, 't', self.player.trade)
            list_available_actions['t'] = '(T)rade'

        if player.curr_hp < 100:
            self.action_adder(actions, 'h', self.player.heal)
            list_available_actions['h'] = '(H)eal up'

        if isinstance(room, world.EnemyTile) and room.enemy.is_alive():
            self.action_adder(actions, 'a', self.player.attack)
            list_available_actions['a'] = '(A)ttack!'
        else:
            if self.player.inventory:
                self.action_adder(actions, 'i', self.player.print_inventory)
                list_available_actions['i'] = 'Show (I)nventory'

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

        self.action_adder(actions, 'x', self.exit_to_main)
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
        list_saves = []
        confirm_save = False

        if not os.path.exists('saves'):
            os.makedirs('saves')

        for idx, save_file in enumerate(os.listdir("saves")):
            if save_file.endswith(".dat"):
                list_saves.append(save_file)

        os.system('cls')

        while confirm_save is False:
            os.system('cls')
            save_name = input("Please enter a filename for the save: ")
            save_name = re.sub(r'\W+', '', save_name)

            if save_name + ".dat" in list_saves:
                overwrite_save = input("Save already exists, overwrite (y/n)? ")

                if overwrite_save == 'y':
                    confirm_save = True
                    pass
            else:
                pass

        pickle.dump(data, open("saves/" + save_name + ".dat", "wb"))
        os.system("cls")
        print("Your progress has been saved!")
        input("Press enter to continue...")
        self.player.room.visited = 0
        self.start_game(self.player, self.map)

    def exit_to_main(self):
        global main_menu
        main_menu = True
        return
