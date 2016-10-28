"""Escape from Cave Terror!"""
import operator
from collections import OrderedDict

from entities.player import Player
import maps.world as world


def play():
    world.parse_world_dsl("maps/level1.map")
    player = Player()
    print("Escape from Cave Terror!")

    while True:
        room = world.tile_at(player.x, player.y)
        print(room.intro_text())
        room.modify_player(player)
        print(room.x + ' ' + room.y)
        choose_action(room, player)

def get_player_command():
    return input('Action: ')

def get_available_actions(room, player, list_available_actions):
    actions = OrderedDict()
    print("\nChoose an action (type '?'' for help):\n")

    if player.inventory:
        action_adder(actions, 'i', player.print_inventory)
        list_available_actions['i'] = 'Show Inventory'
    if isinstance(room, world.EnemyTile) and room.enemy.is_alive():
        action_adder(actions, 'a', player.attack)
        list_available_actions['a'] = 'Attack!'
    else:
        if world.tile_at(room.x, room.y - 1):
            action_adder(actions, 'n', player.move_north)
            list_available_actions['n'] = 'Go north'
        if world.tile_at(room.x, room.y + 1):
            action_adder(actions, 's', player.move_south)
            list_available_actions['s'] = 'Go south'
        if world.tile_at(room.x + 1, room.y):
            action_adder(actions, 'e', player.move_east)
            list_available_actions['e'] = 'Go east'
        if world.tile_at(room.x - 1, room.y):
            action_adder(actions, 'w', player.move_west)
            list_available_actions['w'] = 'Go west'
        if player.hp < 100:
            action_adder(actions, 'h', player.heal)
            list_available_actions['h'] = 'Heal up'

    return actions

def action_adder(action_dict, hotkey, action):
    action_dict[hotkey.lower()] = action
    action_dict[hotkey.upper()] = action

def choose_action(room, player):
    action = None
    list_available_actions = OrderedDict()

    while not action:
        available_actions = get_available_actions(room, player, list_available_actions)
        action_input = input("\nAction: ")
        action = available_actions.get(action_input)

        if action_input == '?':
            for key, name in list_available_actions.items():
                print(key + ': ' + name)
        elif action:
            action()
        else:
            print("You can't do that here")

play()
