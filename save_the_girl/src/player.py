"""Create player entity and define player actions"""

import os
import random
import decimal

import src.weapons as weapons
import src.items as items
import src.world as world


class Player:
    def __init__(self):
        self.room = None
        self.base_class = 'Knight'
        self.inventory = [weapons.Rock(),
                          items.CrustyBread()]
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
        print("----------")

        for item in self.inventory:
            print('    * ' + str(item))

        print('\nGold: {}'.format(self.gold))

        best_weapon = self.most_powerful_weapon()
        print('Best Weapon: {} ({} damage)'.format(best_weapon, best_weapon.damage))

    def most_powerful_weapon(self):
        max_damage = 0
        best_weapon = None

        for item in self. inventory:
            try:
                if item.damage > max_damage:
                    best_weapon = item
                    max_damage = item.damage
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
                    self.inventory.append(weapons.Dagger())

                if enemy.name == "Rock Monster" and random.randrange(1, 3) == 2:
                    print("They also dropped their heavy axe. Sweet!")
                    self.inventory.append(weapons.Dagger())
        else:
            print("{} HP is {}.".format(enemy.name, enemy.hp))

    def heal(self):
        consumables = [item for item in self.inventory if isinstance(item, items.Consumable)]
        heal_choice = None

        if not consumables:
            print("\nYou don't have any items to heal you!\n")
            return

        print("\nHealing Items")
        print("----------------\n")

        for i, item in enumerate(consumables, 1):
            print("    {}: {}".format(i, item))

        print("    q: Back to battle")
        valid = False

        while heal_choice not in consumables:
            heal_choice = input("\nWhich item do you want to use?: ")

            if heal_choice == 'q':
                return
            else:
                try:
                    to_eat = consumables[int(choice) - 1]
                    self.curr_hp = min(self.max_hp, self.curr_hp + to_eat.healing_value)
                    self.inventory.remove(to_eat)
                    print("Current HP: {}".format(self.curr_hp))
                    valid = True
                except (ValueError, IndexError):
                    print("Invalid choice, try again.")

    def trade(self):
        room = self.room
        room.check_if_trade(self)
