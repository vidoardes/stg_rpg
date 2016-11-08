"""Save the Girl!"""

import os
import pickle
from collections import OrderedDict

import src.world as world
from src.engine import GameInit, GameManager
from src.player import Player


def clear():
    return os.system('cls')


def main_menu():
    while True:
        menu_choice = None

        clear()
        print("  __________________________________________________________________________________________ ")
        print(" |  _______                           _______  __                _______  __        __  __  |")
        print(" | |     __|.---.-..--.--..-----.    |_     _||  |--..-----.    |     __||__|.----.|  ||  | |")
        print(" | |__     ||  _  ||  |  ||  -__|      |   |  |     ||  -__|    |    |  ||  ||   _||  ||__| |")
        print(" | |_______||___._| \___/ |_____|      |___|  |__|__||_____|    |_______||__||__|  |__||__| |")
        print(" |__________________________________________________________________________________________|")
        print("  Created by vidoardes                                                          version 0.2a ")
        print("\n   You are \"The Guy\" and everything was great, until \"The Villan\" came along and took your")
        print("    girl! Run through dungeons and battle creatures to rescue \"The Girl\" and save the day!")
        print("\n              (S)tart New Game")
        print("              (L)oad Saved Game")
        print("              (C)redits")
        print("              (Q)uit")

        menu_choice = input('\n>>> ')

        if menu_choice in ['L', 'l']:
            load_game()
        elif menu_choice in ['C', 'c']:
            clear()
            print("                                                                                             ")
            print("                                   CREATED BY VIDO ARDES                                     ")
            print("                                     Copyright (c) 2016                                      ")
            print("                                                                                             ")
            print("                            Open sourced under the MIT License                               ")
            print("               Visit https://github.com/vidoardes/stg_rpg/ for more details!                 ")
            print("                                                                                             ")
            input("")
            main_menu()
        elif menu_choice in ['Q', 'q']:
            clear()
            quit_game = input("Are you sure you want to quit? (Y/N): ")

            if quit_game == 'n':
                main_menu()
            elif quit_game == 'y':
                print("Thanks for playing!")
                exit()
            else:
                main_menu()
        elif menu_choice in ['S', 's']:
            new_game = GameInit()
            setup_player(new_game.player)
            GameManager().start_game(new_game.player, new_game.map)


def setup_player(new_player):
    class_choice = None

    clear()
    print("Pick a class")
    print("------------\n")

    print("1. KNIGHT (Normal)")
    print("110 HP / ATK 90 / DEF 100 / DEX 85 / LUCK 95")
    print("Starting Gold: 10")
    print("A good all rounder whos a jack of all trades, master of none.")
    print("Your bog standard, run of the mill RPG guy.\n")

    print("2. NINJA (Hard)")
    print("75 HP / ATK 60 / DEF 60 / DEX 150 / LUCK 120")
    print("Starting Gold: 5")
    print("Doesn't hit very hard and can't take a punch, but dodges")
    print("like my brother at bill time, and can find loot anywhere.\n")

    print("3. GUARD (Expert)")
    print("140 HP / ATK 55 / DEF 130 / DEX 10 / LUCK 105")
    print("Starting Gold: 0")
    print("He might take a while, but he does the best rope-a-dope around.")
    print("Moves about as fast as your average glacier.\n")

    while class_choice not in ['1', '2', '3']:
        class_choice = input("Choose your class: ")

        if class_choice == '1':
            new_player.base_class = 'Knight'
            new_player.max_hp = 110
            new_player.curr_hp = 110
            new_player.atk_stat = 90
            new_player.def_stat = 100
            new_player.dex_stat = 85
            new_player.luc_stat = 95
            new_player.gold = 10
        elif class_choice == '2':
            new_player.base_class = 'Ninja'
            new_player.max_hp = 75
            new_player.curr_hp = 75
            new_player.atk_stat = 60
            new_player.def_stat = 60
            new_player.dex_stat = 150
            new_player.luc_stat = 120
            new_player.gold = 5
        elif class_choice == '3':
            new_player.base_class = 'Guard'
            new_player.max_hp = 140
            new_player.curr_hp = 140
            new_player.atk_stat = 55
            new_player.def_stat = 130
            new_player.dex_stat = 10
            new_player.luc_stat = 105
            new_player.gold = 10
        else:
            print("Invalid choice!")


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

        for key, value in list_saves.items():
            print("    {}: {}".format(key, value))

        print("    q: Back to main menu")

        while save_choice not in list_saves:
            save_choice = input("\nPlease select which file you wish to load: ")

            if save_choice == 'q':
                main_menu()
            elif save_choice in list_saves:
                load_save = pickle.load(open("saves/" + list_saves[save_choice], "rb"))
                GameManager().start_game(load_save["player"], load_save["map"], True)
            else:
                print("Invalid choice!")
    else:
        clear()
        print("No save file found!")
        input("Press enter to continue...")
        main_menu()


if __name__ == '__main__':
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    main_menu()
