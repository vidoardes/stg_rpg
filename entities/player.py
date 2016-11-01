import random

import entities.weapons as weapons
import entities.items as items
import maps.world as world


class Player:
    def __init__(self):
        self.inventory = [weapons.Rock(),
                          items.CrustyBread()]
        self.x = world.start_tile_location[0]
        self.y = world.start_tile_location[1]
        self.hp = 100
        self.gold = 5
        self.atk_stat = 1
        self.def_stat = 1
        self.dex_stat = 1
        self.luc_stat = 1
        self.victory = False

    def is_alive(self):
        return self.hp > 0

    def move(self, dx, dy):
        world.tile_at(self.x, self.y).visited = 0
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
        print("\nInventory:")
        print("----------")

        for item in self.inventory:
            print('    * ' + str(item))

        print('\nGold: {}'.format(self.gold))

        best_weapon = self.most_powerful_weapon()
        print('Best Weapon: {}'.format(best_weapon))

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
        room = world.tile_at(self.x, self.y)
        enemy = room.enemy
        dodge_chance = random.random()
        miss_chance = random.random()

        if miss_chance > 0.98:
            print("You missed your attack!")
        elif dodge_chance > 0.98:
            print(enemy.Name + " dodged the attack!")
        else:
            print("\nYou use a {} against the {}!".format(best_weapon.name, enemy.name))
            enemy.hp -= best_weapon.damage

        if not enemy.is_alive():
            print("\nYou killed {}!".format(enemy.name))
        else:
            print("{} HP is {}.".format(enemy.name, enemy.hp))

    def heal(self):
        consumables = [item for item in self.inventory if isinstance(item, items.Consumable)]

        if not consumables:
            print("You don't have any items to heal you!")
            return

        for i, item in enumerate(consumables, 1):
            print("Choose an item to use to heal: ")
            print("{}. {}".format(i, item))
            valid = False

            while not valid:
                choice = input("")
                try:
                    to_eat = consumables[int(choice) - 1]
                    self.hp = min(100, self.hp + to_eat.healing_value)
                    self.inventory.remove(to_eat)
                    print("Current HP: {}".format(self.hp))
                    valid = True
                except (ValueError, IndexError):
                    print("Invalid choice, try again.")
    
    def trade(self):
        room = world.tile_at(self.x, self.y)
        room.check_if_trade(self)
