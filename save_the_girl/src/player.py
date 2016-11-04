"""Create player entity and define player actions"""

import os
import json
import random
import decimal

import src.items as items
import src.world as world
import src.weapons as weapons


class Player:
    def __init__(self):
        self.room = None
        self.name = "Unnamed Soldier"
        self.base_class = "Knight"
        self.inventory = {
            "Weapons": {
                "Rock": {"obj": weapons.Rock(), "qty": 1}
            },
            "Items": {
                "Crusty Bread": {"obj": items.CrustyBread(), "qty": 1}
            }
        }
        self.x = world.start_tile_location[0]
        self.y = world.start_tile_location[1]
        self.curr_hp = 100
        self.max_hp = 100
        self.gold = 5
        self.atk_stat = 100
        self.def_stat = 100
        self.dex_stat = 100
        self.luc_stat = 100
        self.victory = False

    def __str__(self):
        return "Player\n HP: {} / ATK: {} / DEF: {} / DEX: {} / LUCK: {}".format(
            self.curr_hp, self.atk_stat, self.def_stat, self.dex_stat, self.luc_stat)

    def is_alive(self):
        return self.curr_hp > 0

    def move(self, dx, dy):
        self.room.visited = 0
        self.x += dx
        self.y += dy

    def move_north(self):
        self.move(dx=0, dy=-1)

    def move_south(self):
        self.move(dx=0, dy=1)

    def move_east(self):
        self.move(dx=1, dy=0)

    def move_west(self):
        self.move(dx=-1, dy=0)

    def print_inventory(self):
        os.system('cls')
        print("{}'s Inventory:".format(self.base_class))
        print("{} / {} HP".format(self.curr_hp, self.max_hp))
        print("----------\n")

        for item_cat, item_attr in self.inventory['Items'].items():
            if item_attr["qty"] > 0:
                print('    * {} x{}'.format(item_cat, item_attr["qty"]))

        print('\n{} Gold'.format(self.gold))

        best_weapon = self.most_powerful_weapon()
        print('Best Weapon: {} ({} damage)'.format(best_weapon, best_weapon.damage))

    def most_powerful_weapon(self):
        max_damage = 0
        best_weapon = None

        for weapon_cat, weapon_attr in self.inventory['Weapons'].items():
            try:
                if weapon_attr["obj"].damage > max_damage:
                    best_weapon = weapon_attr["obj"]
                    max_damage = weapon_attr["obj"].damage
            except AttributeError:
                pass

        return best_weapon

    def attack(self):
        best_weapon = self.most_powerful_weapon()
        room = self.room
        enemy = room.enemy
        luck_mod = decimal.Decimal(2 - (self.luc_stat / 100))
        dodge_chance = decimal.Decimal(random.random()) * luck_mod
        miss_chance = decimal.Decimal(random.random()) * luck_mod

        if miss_chance > 0.98:
            print("You missed your attack!")
        elif dodge_chance > 0.98:
            print("{} dodged the attack!".format(enemy.name))
        else:
            print("\nYou use a {} against the {}!".format(best_weapon.name, enemy.name))
            atk_mod = decimal.Decimal(self.atk_stat / 100)
            weapon_dmg = round(best_weapon.damage * atk_mod, 0)
            enemy.hp -= weapon_dmg

        if not enemy.is_alive():
            os.system('cls')
            print("\n  ____   ____.___ _________  ___________________   __________ _____.___.._.")
            print("  \\   \\ /   /|   |\\_   ___ \\ \\__    ___/\\_____  \\  \\______   \\\\__  |   || |")
            print("   \\   Y   / |   |/    \\  \\/   |    |    /   |   \\  |       _/ /   |   || |")
            print("    \\     /  |   |\\     \\____  |    |   /    |    \\ |    |   \\ \\____   | \\|")
            print("     \\___/   |___| \\______  /  |____|   \\_______  / |____|_  / / ______| __")
            print("                          \\/                    \\/         \\/  \\/        \\/")
            print("\nYou killed the {}!".format(enemy.name))

            loot_chance = random.randrange(1, 4)

            if loot_chance == 3:
                luc_mod = decimal.Decimal((self.luc_stat / 100))
                enemy_loot = round(enemy.loot * luc_mod, 0)
                self.gold += enemy_loot
                print("They dropped some loot! You recieved {} gold.".format(enemy_loot))

                if enemy.name == "Goblin" and random.randrange(1, 3) == 2:
                    print("They also dropped their dagger. Sweet!")

                    if weapons.Dagger.name in self.inventory['Weapons'].items():
                        for weapon_cat, weapon_attr in self.inventory['Weapons'].items():
                            if item_cat == weapons.Dagger.name:
                                item_attr["qty"] += 1
                    else:
                        self.inventory['Weapons'][weapons.Dagger.name] = {}
                        self.inventory['Weapons'][weapons.Dagger.name]['obj'] = weapons.Dagger
                        self.inventory['Weapons'][weapons.Dagger.name]['qty'] = 1

                if enemy.name == "Rock Monster" and random.randrange(1, 3) == 2:
                    print("They also dropped their heavy axe. Sweet!")

                    if weapons.HeavyAxe.name in self.inventory['Weapons'].items():
                        for weapon_cat, weapon_attr in self.inventory['Weapons'].items():
                            if item_cat == weapons.HeavyAxe.name:
                                item_attr["qty"] += 1
                    else:
                        self.inventory['Weapons'][weapons.Dagger.name] = {}
                        self.inventory['Weapons'][weapons.Dagger.name]['obj'] = weapons.HeavyAxe
                        self.inventory['Weapons'][weapons.Dagger.name]['qty'] = 1
        else:
            print("{} HP is {}.".format(enemy.name, enemy.hp))

    def heal(self):
        heal_choice = None
        consumables = []

        for item_cat, item_attr in self.inventory['Items'].items():
            if isinstance(item_attr["obj"], items.Consumable) and item_attr['qty'] > 0:
                consumables.append(item_attr["obj"])

        print("\nHealing Items")
        print("----------------\n")

        if not consumables:
            print("You don't have any items to heal you!")
        else:
            for i, item in enumerate(consumables, 1):
                print("    {}: {}".format(i, item.name))

        print("\nq: Back to battle")

        while heal_choice not in consumables:
            heal_choice = input("\nWhich item do you want to use?: ")

            if heal_choice in ['Q', 'q']:
                self.room.visited = 0
                return
            else:
                try:
                    to_eat = consumables[int(heal_choice) - 1]
                    self.curr_hp = min(self.max_hp, self.curr_hp + to_eat.healing_value)
                    for item_cat, item_attr in self.inventory['Items'].items():
                        if item_cat == item.name:
                            item_attr["qty"] -= 1
                            self.room.visited = 0
                            return

                    print("HP: {} / {}".format(self.curr_hp, self.max_hp))
                except (ValueError, IndexError):
                    print("Invalid choice!")

    def trade(self):
        room = self.room
        room.check_if_trade(self)
